import os
import torch
import torchvision

from math import ceil
from io import BytesIO

from typing import Optional
from bson import ObjectId

from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info

from models.search import Search, Question

from models.requests.search import SearchRequest, FollowUpQuestionRequest
from models.responses.answer import SearchResponse

from repositories.search_repositories import SearchRepository, QuestionRepository

from services.amazon_service import AmazonService

from logger import logger

class SearchService:
    def __init__(self, search_repository: SearchRepository, question_repository: QuestionRepository, amazon_service: AmazonService, model: Qwen2VLForConditionalGeneration, processor: AutoProcessor):
        self.model = model
        self.processor = processor
        self.amazon_service = amazon_service
        self.search_repository = search_repository
        self.question_repository = question_repository

    def generate_answer(self, search_request: SearchRequest) -> Optional[SearchResponse]:
        search = self.search_repository.create_search(search_request)
        question = self.create_question(search)

        # TODO: implement answer generation

        answer = ""
        token = 0

        self.update_question_answer(question.id, answer, token, search.created_by)

        response = SearchResponse(
            search=search.id,
            asset=search.asset,
            question=search.title,
            answer=answer,
            token=token,
            status=QuestionStatus.ANSWERED.value,
            created_by=search.created_by,
            updated_by=search.created_by,
            created_date=search.created_date,
            updated_date=search.updated_date
        )

        return response


    def create_search(self, search_request: SearchRequest) -> Search:
        return self.search_repository.create_search({"asset": search_request.asset, "title": search_request.question}, search_request.fingerprint)

    def create_question(self, search: Search) -> Question:
        return self.question_repository.create_question({"search": search.id, "asset": search.asset, "question": search.title}, search.created_by)

    def update_question_answer(self, question_id: ObjectId, answer: str, token: int, updated_by: str) -> Question:
        return self.question_repository.update_question_answer(question_id, answer, token, updated_by)


    # def generate_answer(self, search_answer_request: SearchAnswerRequest) -> SearchAnswerResponse | None:

    #     try:

    #         logger.debug(f"generating answer for query {search_answer_request.query}")

    #         messages = self.generate_prompts_for_video(search_answer_request)
    #         text = self.processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

    #         image_inputs, video_inputs = process_vision_info(messages)
    #         inputs = self.processor(
    #             text=[text],
    #             images=image_inputs,
    #             videos=video_inputs,
    #                 padding=True,
    #                 return_tensors="pt",
    #         )

    #         with torch.no_grad():
    #             generated_ids = self.model.generate(**inputs)

    #         # trim the generated output to remove the input prompt
    #         generated_ids_trimmed = [out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)]

    #         # Decode the generated text
    #         output_text = self.processor.batch_decode(generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False)

    #         torch.cuda.empty_cache()

    #         response = SearchAnswerResponse(query=search_answer_request.query, answer=output_text)
    #         return response

    #     except Exception as err:
    #         logger.error(f"failed to generate answer for query {search_answer_request.query} {err.__str__()}")

    # def generate_prompts_for_video(self, search_answer_request: SearchAnswerRequest):

    #     video_frames = self.get_frames()

    #     messages = [{
    #         "role": "user",
    #         "content": [{
    #             "type": "video",
    #             "video": video_frames,
    #             "max_pixels": 360 * 420,
    #             "fps": 1.0
    #         }, {
    #             "type": "text",
    #             "text": search_answer_request.query
    #         }]
    #     }]

    #     return messages

    # @staticmethod
    # def get_frames(fraction=0.0125):
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