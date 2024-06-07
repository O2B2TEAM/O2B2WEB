import base64
import io
import time

import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from PIL import Image

# GPT-4 모델을 호출하는 llm 객체 생성
llm = ChatOpenAI(api_key="sk-proj-yhsg5NrooNlcqRhn9sjkT3BlbkFJPVlyezvH9aCm3c4LlHeH")

# 프롬프트 템플릿 설정 (한글로)
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 개발자 전문 이력서 작성자입니다. 전문적인 이력서를 작성해 주세요."),
    ("user", "이름: {name}\n직무: {jobs}\n시작 연도: {start_year}\n종료 연도: {end_year}\n연락처: {contact}\n학력: {education}\n자격증: {cert}\nURL: {url}\n회사: {company}\n경력: {experience}\n기술: {skills}\n기술 레벨: {skill_levels}\n자기소개: {summary}\n"),
    ("system", "직무의 특징, gihub 링크 정보 분석, 자격증과 skill을 분석해서 이력서를 3000자 이상으로 작성해줘. 기술 부분을 더 자세히 작성해줘. 맨 위에 누구의 이력서인지 나오게 해 줘. 문서 마지막엔 '감사합니다'를 항상 포함해줘. 경력 관련 내용도 추정해서 길게 써줘")
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

# 생성된 이력서 출력
img_data = base64.b64decode(st.session_state.uploaded_image)
st.image(Image.open(io.BytesIO(img_data)))
st.write(result)

# session_state에 result를 저장
st.session_state.result = result