# LangChain을 이용항 이미지 생성
- 이미지 생성모델로 'runwayml/stable-diffusion-v1-5' 사용
- 첫 실행 시 이미지 생성모델 다운로드 자동실행
- openai 모델로 'gpt-3.5-turbo' 사용  
- cpu로 돌리기 때문에 시간이 굉장히 오래 걸림 (추후 cuda로 돌리는 코드 업로드 예정)
- 사용환경: Mac M2

## 1. 사전준비
- 로그인 기능을 이용하기 위해서는 .streamlit 폴더 내 credentials.yaml 파일을 만들어서 로그인 내용 추가 필요
- credentials.yaml을 만들기 위해 login_pass.py 먼저 실행
- requirments.txt 파일을 통해 필요한 패키지들을 모두 설치

## 2. main.py 실행
- 터미널에 streamlit run main.py 실행
- 생성되는 로컬 url을 통해 웹페이지 확인
- image generator에 이미지 업로드
- 원하는 이미지 생성개수 설정 (최소2개~최대8개)
- 생성된 이미지는 images 폴더로 임시저장됨 새로고침을 하거나 원본이미지를 변경, 삭제하면 생성된 이미지도 삭제됨

- image editor는 추후 코드 업로드 예정