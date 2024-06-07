import base64
import io

import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from PIL import Image

# GPT-4 모델을 호출하는 llm 객체 생성
llm = ChatOpenAI(api_key="sk-proj-yhsg5NrooNlcqRhn9sjkT3BlbkFJPVlyezvH9aCm3c4LlHeH")

st.header("노세老世 | AI HR", divider='orange')
st.subheader("이력서 생성기")
st.markdown(" ")

col1, col3 = st.columns([2, 1])

with col1:
    name = st.text_input("이름")
    # Jobs 입력 받기 (여러 개 선택 가능)
    jobs = st.multiselect(
        "직무",
        ["DevOps/시스템 관리자", "HW/임베디드 개발자", "IOS 개발자",
        "데이터 사이언티스트", "데이터 엔지니어", "서버/백엔드 개발자",
        "안드로이드 개발자", "프론트엔드 개발자", "게임 서버 개발자",
        "게임 클라이언트 개발자"])

    start_year, end_year = st.select_slider(
        "경력을 입력 해 주세요",
        options=["신입", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15년 이상"],
        value=("신입", "15년 이상"))

with col3:
    st.image("images/image_resume.png")
    st.markdown("반가워요. 당신의 이력서를 생성 해 드립니다.")

st.markdown("---")

col1,col2,col3=st.columns(3)
with col1:
    uploaded_files = st.file_uploader("증명사진을 첨부 해 주세요", type=["png", "jpg", "jpeg"], accept_multiple_files=True)# 사용자가 여러 파일을 업로드할 수 있도록 허용

    if uploaded_files:
        for uploaded_file in uploaded_files:
            bytes_data = uploaded_file.read()        # 파일을 바이트로 읽기
            image = Image.open(io.BytesIO(bytes_data))        # PIL을 사용하여 이미지 로드
            resized_image = image.resize((103, 132))        # 이미지를 103x132 픽셀로 크기 조정
            
            # 이미지 데이터를 base64로 인코딩하여 session state에 저장
            buffered = io.BytesIO()
            resized_image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            st.session_state.uploaded_image = img_str
            
            st.image(resized_image)        # 이미지 표시

with col2:
    contact = st.text_input("연락처")
    education = st.text_input("대학교, 학과")
    cert=st.text_area("자격증")   

with col3:
    url = st.text_input("github 주소")
    company = st.text_input("(구)직장명")  
    experience = st.text_area("경력")

skills=st.multiselect("기술",[    "Python", "JavaScript", "Java", "C#", "C++", "Ruby", "Swift", 
"Kotlin", "Go", "Rust", "SQL", "R", "PHP", "HTML", "CSS", 
"TypeScript", "Scala", "Perl", "Matlab", "SAS"])

skill_levels = {}
for skill in skills:
    level = st.radio(f"{skill} 레벨 선택", ["상", "중", "하"], key=f"level_{skill}")
    skill_levels[skill] = level

summary = st.text_area("자기소개")

if 'name' not in st.session_state:
    st.session_state.name = ""
if 'jobs' not in st.session_state:
    st.session_state.jobs = []
if 'start_year' not in st.session_state:
    st.session_state.start_year = ""
if 'end_year' not in st.session_state:
    st.session_state.end_year = ""
if 'contact' not in st.session_state:
    st.session_state.contact = ""
if 'education' not in st.session_state:
    st.session_state.education = ""
if 'cert' not in st.session_state:
    st.session_state.cert = ""
if 'url' not in st.session_state:
    st.session_state.url = ""
if 'company' not in st.session_state:
    st.session_state.company = ""
if 'experience' not in st.session_state:
    st.session_state.experience = ""
if 'skills' not in st.session_state:
    st.session_state.skills = []
if 'skill_levels' not in st.session_state:
    st.session_state.skill_levels = {}
if 'summary' not in st.session_state:
    st.session_state.summary = ""

st.session_state.name = name
st.session_state.jobs = jobs
st.session_state.start_year = start_year
st.session_state.end_year = end_year
st.session_state.contact = contact
st.session_state.education = education
st.session_state.cert = cert  # Added to include certification if available
st.session_state.url = url
st.session_state.company = company
st.session_state.experience = experience
st.session_state.skills = skills
st.session_state.skill_levels = skill_levels
st.session_state.summary = summary

# 페이지 이동 버튼
st.page_link("pages/resume_maked.py", label="이력서 생성하기")

# 확인용 결과창
if st.button('결과 출력'):
    st.markdown("### 결과:")
    st.write(f"name: {st.session_state.name}")
    st.write(f"jobs: {st.session_state.jobs}")
    st.write(f"start_year: {st.session_state.start_year}")
    st.write(f"end_year: {st.session_state.end_year}")
    st.write(f"contact: {st.session_state.contact}")
    st.write(f"education: {st.session_state.education}")
    st.write(f"cert: {st.session_state.cert}")
    st.write(f"url: {st.session_state.url}")
    st.write(f"company: {st.session_state.company}")
    st.write(f"experience: {st.session_state.experience}")
    st.write(f"skills: {st.session_state.skills}")
    st.write(f"skill_levels: {st.session_state.skill_levels}")
    st.write(f"summary: {st.session_state.summary}")

    if st.session_state.uploaded_image:
        st.markdown("#### 증명사진:")
        # base64로 인코딩된 이미지 데이터를 디코딩하여 표시
        img_data = base64.b64decode(st.session_state.uploaded_image)
        st.image(Image.open(io.BytesIO(img_data)))

st.markdown("---")
