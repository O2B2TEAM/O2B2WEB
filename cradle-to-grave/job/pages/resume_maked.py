import base64
import io
import os
import time

import streamlit as st
from dotenv import load_dotenv
from fpdf import FPDF
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from PIL import Image
from pymongo import MongoClient

# 환경 변수 로드
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="노세老世",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# MongoDB 클라이언트 생성
client = MongoClient("mongodb+srv://test:1234@cluster.ct8weib.mongodb.net/o2b2data?retryWrites=true&w=majority")
db = client["o2b2data"]
collection = db["resume_user"]

# GPT-4 모델을 호출하는 llm 객체 생성
llm = ChatOpenAI(api_key=openai_api_key)

# 프롬프트 템플릿 설정 (한글로)
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 개발자 전문 이력서 작성자입니다. 전문적인 이력서를 작성해 주세요."),
    ("user", "이름: {name}\n직무: {jobs}\n시작 연도: {start_year}\n종료 연도: {end_year}\n연락처: {contact}\n학력: {education}\n자격증: {cert}\nURL: {url}\n회사: {company}\n경력: {experience}\n기술: {skills}\n기술 레벨: {skill_levels}\n자기소개: {summary}\n"),
    ("system", "제목은 '이름의 이력서'라는 제목으로 13pt 로 출력해줘. 다른 내용은 전부 11pt 로 출력해줘. 시작 연도와 종료 연도에 따라 이 개발자의 역량이 어느정도인지 추정해서 작성해줘. 그리고 보유한 자격증에 따라 역량을 추정해서 작성해줘. 그리고 가지고 있는 기술과 기술레벨에 따라 역량이 어느정도인지 추정해서 작성해줘. 마지막에는 '감사합니다'라는 말을 넣어줘. 직무분야, 기술레벨과 경력에 관한 이야기는 꼭 들어가야 해. 경력이 신입이면 신입 수준인 것에 대하여 작성해줘. 그리고 학과도 분석해줘. 가능한 길게 작성해줘. 자기소개는 내용이 없어도 다른 정보들을 조합해서 작성해줘. 자기소개는 '저는'으로 시작해줘")
])

# 출력 파서 생성 (GPT-4의 출력을 문자열로 파싱)
output_parser = StrOutputParser()

# 프롬프트 템플릿, GPT-4 모델, 출력 파서를 체인으로 연결
chain = prompt | llm | output_parser

# 세션 상태에서 데이터 읽기
name = st.session_state.get('name', "")
jobs = st.session_state.get('jobs', "")
uploaded_image = st.session_state.get('uploaded_image', None)  # 이미지 데이터 받기
start_year = st.session_state.get('start_year', "신입")
end_year = st.session_state.get('end_year', "15년 이상")
company = st.session_state.get('company', "")
url = st.session_state.get('url', "")
contact = st.session_state.get('contact', "")
education = st.session_state.get('education', "")
cert = st.session_state.get('cert', "")
experience = st.session_state.get('experience', "")
skills = st.session_state.get('skills', "")
skill_levels = st.session_state.get('skill_levels', "")
summary = st.session_state.get('summary', "")

# end_year를 숫자로 변환
end_year_map = {
    "신입": 0,
    "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
    "7": 7, "8": 8, "9": 9, "10": 10, "11": 11, "12": 12,
    "13": 13, "14": 14, "15년 이상": 15
}
end_year_numeric = end_year_map.get(end_year, 15)

# 버튼이 눌리면 '작성 중입니다...'라는 메시지와 함께 스피너 표시
with st.spinner('작성 중입니다...'):
    # 생성된 이력서를 화면에 출력
    # 체인을 호출하여 사용자가 입력한 내용을 기반으로 GPT-4 모델을 호출하고 결과를 생성
    input_data = {
        "name": name,
        "jobs": jobs,
        "start_year": start_year,
        "end_year": end_year,
        "uploaded_image": uploaded_image,  # 이미지 데이터 전달
        "contact": contact,
        "education": education,
        "cert": cert,
        "url": url,
        "company": company,
        "experience": experience,
        "skills": skills,
        "skill_levels": skill_levels,
        "summary": summary,
    }
    result = chain.invoke(input_data)

    # MongoDB에 데이터 저장
    resume_data = {
        "name": name,
        "jobs": jobs,
        "start_year": start_year,
        "end_year": end_year_numeric,  # 숫자로 변환된 end_year
        "contact": contact,
        "education": education,
        "cert": cert,
        "url": url,
        "company": company,
        "experience": experience,
        "skills": skills,
        "skill_levels": skill_levels,
        "summary": summary,
        "resume_text": result  # AI가 생성한 이력서 텍스트 저장
    }
    collection.insert_one(resume_data)

col1, col2 = st.columns(2)
with col1:
    st.write(result)
with col2:
    img_data = base64.b64decode(uploaded_image)
    st.image(Image.open(io.BytesIO(img_data)))

# PDF 생성 함수
def create_pdf(resume_text):
    pdf = FPDF()
    pdf.add_page()

    pdf.add_font("DejaVu", "", "DejaVuSansCondensed.ttf", uni=True)
    pdf.set_font("DejaVu", size=11)

    for line in resume_text.split('\n'):
        pdf.cell(200, 10, txt=line, ln=True)

    return pdf

# PDF 다운로드 버튼 생성
if st.button("PDF 다운로드"):
    pdf = create_pdf(result)
    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    b64 = base64.b64encode(pdf_output.read()).decode('utf-8')
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="resume.pdf">여기를 클릭하여 PDF 다운로드</a>'
    st.markdown(href, unsafe_allow_html=True)

st.markdown("---")
