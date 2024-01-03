import streamlit as st
from st_pages import add_page_title
import streamlit.components.v1 as components

import os
import shutil
from PIL import Image, ImageOps
from utils.util import resize_image
from utils.agents import image_generator_agent
from utils.template import image_generate_template



def image_generator():
    add_page_title()

    # 이미지 생성값 초기화
    if "generted_image" not in st.session_state:
        st.session_state["generted_image"] = False

    # 이미지 업로드
    uploaded_file = st.file_uploader("이미지 업로드", type=["png", "jpg"])
    if uploaded_file is not None:

        # 이미지 생성 갯수 설정
        num_images = st.slider('이미지 생성 개수 설정', 1, 8, 2)

        # show 원본 이미지
        if uploaded_file is not None:
            image = Image.open(uploaded_file).convert('RGB')
            image = ImageOps.exif_transpose(image) # 이미지 자동회전 금지
            resized_image, _ = resize_image(image, max_width=704, max_height=704)
            st.markdown("#### Origin Image")
            st.image(resized_image)

        # 텍스트 입력
        prompt = st.chat_input("Send a message")

        # 생성모델에 이미지 생성 요청
        if prompt:
            with st.chat_message('assistant'):
                st.write('AI')
                with st.spinner(text='In progress...'):
                    agent = image_generator_agent()
                    agent(image_generate_template(prompt=prompt, num_images=num_images))
                    st.session_state["generted_image"] = True
                    st.experimental_rerun()

        # show generated image
        if st.session_state['generted_image']:
            st.markdown('#### Generated Image')
            imageUrls = [f'./images/'+ i for i in os.listdir('./images')]
            for img in imageUrls:
                image = Image.open(img).convert('RGB')
                image = ImageOps.exif_transpose(image) # 이미지 자동회전 금지
                resized_image, _ = resize_image(image, max_width=704, max_height=704)
                st.session_state['generated_image'] = resized_image
                st.image(st.session_state['generated_image'])

    else:
        st.session_state.clear()
        if os.path.exists('images'):
            shutil.rmtree('images')
            print('image폴더삭제')

if __name__ == "__main__":
    image_generator()