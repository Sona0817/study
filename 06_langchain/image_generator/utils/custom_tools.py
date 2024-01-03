from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Optional, Type
from utils.generator_functions import general_generator

import os
import shutil
import streamlit as st
import torch

class ImageGeneratorCheckInput(BaseModel):
    prompt: str = Field(..., description='prompt for generating image')
    num_images: int = Field(..., description='number of images to generate')
    device: str = Field(..., description='use cpu or gpu cuda')

class ImageGeneratorTool(BaseTool):
    name = 'general_generator'
    description='''please use this tool when you want to generate images.'''

    def _run(self, prompt:str, num_images:int, device:str):
        
        # 기존의 image 파일 모두 삭제
        shutil.rmtree("./images", ignore_errors=True)

        # 이미지 저장할 폴더 생성
        os.makedirs('./images', exist_ok=True)

        images = general_generator(prompt, num_images, device)

        for idx, image in enumerate(images):
            image.save(f'./images/{idx}.png')

        if device=='cuda':
            torch.cuda.empty_cache()

        return 'complete!'
    
    def _arun(self, query: str):
        raise NotImplementedError('This tool does not support async')
    
    args_schema: Optional[Type[BaseModel]] = ImageGeneratorCheckInput
