import os
import torch
import torchvision

from math import ceil
from io import BytesIO

from typing import Optional, Tuple
from bson import ObjectId

from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info

from models.conversation.chat import Chat
from models.requests.search import GetAnswerRequest
from models.responses.answer import SearchAnswerResponse

from repositories.conversation.conversation_repository import ConversationRepository
from repositories.conversation.chat_repository import ChatRepository

from services.amazon_service import AmazonService

from logger import logger

class SearchService:
    def __init__(self, conversation_repository: ConversationRepository, chat_repository: ChatRepository, amazon_service: AmazonService, model: Qwen2VLForConditionalGeneration, processor: AutoProcessor):
        self.conversation_repository = conversation_repository
        self.chat_repository = chat_repository
        
        self.model = model
        self.processor = processor
        self.amazon_service = amazon_service

    def generate_answer(self, request: GetAnswerRequest) -> Optional[SearchAnswerResponse]:
        try:

            logger.debug(f"received request to generate answer: {request.question}")

            # Get or create a conversation
            conversation_id = request.conversation or self.create_conversation(request)
            logger.debug(f"using conversation id: {conversation_id}")

            # Create a new chat entry
            chat_id = self.create_chat(conversation_id, request)
            logger.debug(f"created new chat with id: {chat_id}")

            # Generate response based on the question and asset
            answer, token = self.generate_answer_for_chat(chat_id)
            logger.info(f"generated response with {token} tokens")

            # Update the chat with the generated answer
            self.update_answer(chat_id, answer, token)
            logger.debug(f"updated chat {chat_id} with answer")

            # Construct and return the response
            return SearchAnswerResponse(
                id=chat_id,
                conversation=conversation_id,
                question=request.question,
                answer=answer,
                token=token
            )

        except Exception as e:
            logger.error(f"error generating answer: {str(e)}")
            return None

    def create_conversation(self, request: GetAnswerRequest) -> str:
        return self.conversation_repository.create_conversation({
            "title": request.question,
            "assets": [ObjectId(request.asset)]
        }, request.fingerprint)

    def create_chat(self, conversation_id: str, request: GetAnswerRequest) -> str:
        return self.chat_repository.create_chat({
            "conversation": ObjectId(conversation_id),
            "question": request.question,
            "assets": [ObjectId(request.asset)]
        }, request.fingerprint)

    def update_answer(self, chat_id: str, answer: str, token: int) -> bool:
        updated = self.chat_repository.update_chat(chat_id, {"$set": {"answer": answer, "token": token}} )
        if not updated:
            logger.error(f"Failed to update answer for chat {chat_id}")

        return updated

    def generate_answer_for_chat(self, chat: Chat) -> Tuple[str, int]:
        try:
            logger.info(f"Generating answer for chat ID: {chat.id}")
            
            # prepare input for the model
            messages = self.generate_prompts_for_video(chat)
            text = self.processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            image_inputs, video_inputs = process_vision_info(messages)
            
            inputs = self.processor(
                text=[text],
                images=image_inputs,
                videos=video_inputs,
                padding=True,
                return_tensors="pt"
            )
            
            # generate response
            with torch.no_grad():
                generated_ids = self.model.generate(**inputs)
            
            # post-process the generated output
            generated_ids_trimmed = [out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)]
            output_text = self.processor.batch_decode(generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False)
            
            # clean up GPU memory
            torch.cuda.empty_cache()
            
            logger.info(f"successfully generated answer for chat ID: {chat.id}")
            return output_text[0], output_text[1]  # assuming output_text is a list with one item
        
        except Exception as err:
            logger.error(f"failed to generate answer for chat ID {chat.id}: {err}", exc_info=True)
            return None

    def generate_prompts_for_video(self, chat: Chat):
        return [{
            "role": "user",
            "content": [
                {
                    "type": "video",
                    "video": self.get_frames(),
                    "max_pixels": 151200,  # 360 * 420
                    "fps": 1.0
                },
                {
                    "type": "text",
                    "text": chat.question
                }
            ]
        }]

    @staticmethod
    def get_frames(fraction=0.0125):
        frames_path = "./documents/data/frames"
        all_frames = sorted([f for f in os.listdir(frames_path) if f.endswith('.jpg')])

        total_frames = len(all_frames)
        frames_to_keep = ceil(total_frames * fraction)

        # calculate the step size to evenly distribute the selected frames
        step = total_frames // frames_to_keep

        # select the frames
        selected_frames = all_frames[::step][:frames_to_keep]

        # create the full paths for the selected frames
        frame_paths = [f"file://{os.path.join(frames_path, frame)}" for frame in selected_frames]

        return frame_paths