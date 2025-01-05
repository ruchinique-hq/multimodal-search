import os
import torch
import torchvision

from math import ceil
from io import BytesIO

from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info

from services.amazon_service import AmazonService

from models.requests.search import SearchAnswerRequest
from models.responses.answer import SearchAnswerResponse

from logger import logger

class SearchService:
    def __init__(self, amazon_service: AmazonService, model: Qwen2VLForConditionalGeneration, processor: AutoProcessor):
        self.model = model
        self.processor = processor
        self.amazon_service = amazon_service

    def generate_answer(self, search_answer_request: SearchAnswerRequest) -> SearchAnswerResponse | None:

        try:

            logger.debug(f"generating answer for query {search_answer_request.query}")

            messages = self.generate_prompts_for_video(search_answer_request)
            text = self.processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

            image_inputs, video_inputs = process_vision_info(messages)
            inputs = self.processor(
                text=[text],
                images=image_inputs,
                videos=video_inputs,
                    padding=True,
                    return_tensors="pt",
            )

            with torch.no_grad():
                generated_ids = self.model.generate(**inputs)

            # trim the generated output to remove the input prompt
            generated_ids_trimmed = [out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)]

            # Decode the generated text
            output_text = self.processor.batch_decode(generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False)

            torch.cuda.empty_cache()

            response = SearchAnswerResponse(query=search_answer_request.query, answer=output_text)
            return response

        except Exception as err:
            logger.error(f"failed to generate answer for query {search_answer_request.query} {err.__str__()}")


    def generate_prompts_for_video(self, search_answer_request: SearchAnswerRequest):

        video_frames = self.get_frames()

        messages = [{
            "role": "user",
            "content": [{
                "type": "video",
                "video": video_frames,
                "max_pixels": 360 * 420,
                "fps": 1.0
            }, {
                "type": "text",
                "text": search_answer_request.query
            }]
        }]

        return messages

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