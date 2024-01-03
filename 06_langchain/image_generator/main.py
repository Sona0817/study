import streamlit as st
import streamlit_authenticator as stauth
from st_pages import show_pages_from_config, add_page_title

import os
from dotenv import load_dotenv
import yaml
from yaml.loader import SafeLoader

import openai

def main():
    # 로그인 환경설정
    hide_bar= """
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
            visibility:hidden;
            width: 0px;
        }
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
            visibility:hidden;
        }
        </style>
    # """

    with open('.streamlit/credentials.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
        
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
    )

    # 로그인 화면
    name, authentication_status, username = authenticator.login('Login', 'main')

    # 로그인 시도    
    if authentication_status == False:
        st.error("Username/password is incorrect")
        st.markdown(hide_bar, unsafe_allow_html=True)

    elif authentication_status == None:
        st.warning("Please enter your username and password")
        st.markdown(hide_bar, unsafe_allow_html=True)
        
    # Success Login to Main Page
    elif authentication_status:        

        # 로그인 후 openai 연결            
        load_dotenv()
        
        if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
            print("OPENAI_API_KEY is not set")
            exit(1)
        else:
            openai.api_key = os.getenv("OPENAI_API_KEY")
            print("OPENAI_API_KEY is set")

        # Sidebar
        authenticator.logout('Logout', 'sidebar')
        st.sidebar.title(f'Welcome {username}')
        show_pages_from_config(".streamlit/pages.toml")

        # Main
        add_page_title()
        
        st.write("")
        tab1, tab2 = st.tabs(["Image Editor", "Image Generator"])
        
        with tab1:
            st.markdown(
                """
                ##### Image Editor
                Drawing Tool과 채팅을 통해 이미지에서 객체를 바꾸거나 지우고, 이미지 스타일을 변환할 수 있습니다.
                """
            )
            
        with tab2:
            st.markdown(
                """
                ##### Image Generator
                원하는 스타일의 이미지를 업로드하거나 문장을 통해 새로운 이미지를 생성할 수 있습니다.
                """
            )

if __name__ == "__main__":
    main()
    
    
