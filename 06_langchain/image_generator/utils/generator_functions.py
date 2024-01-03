import streamlit as st
import torch
from diffusers import StableDiffusionPipeline

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

@st.cache_resource # 이전에 계산해본적 있는 동일한 입력이 들어왔을 때 계산된 결과를 반환
def get_general_generator(device=device):
    pipeline = StableDiffusionPipeline.from_pretrained('runwayml/stable-diffusion-v1-5')
    
    return pipeline

def general_generator(prompt, num_images, device=device):
    pipeline = get_general_generator(device=device)
    images = pipeline(prompt=prompt,
                      guidance_scale=7,
                      num_inference_steps=20,
                      num_images_per_prompt=num_images,
                     ).images
    
    return images