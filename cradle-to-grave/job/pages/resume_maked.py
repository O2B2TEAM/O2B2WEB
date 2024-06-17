import base64
import io
import os
import time

import sys

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
#    img_data = base64.b64decode(uploaded_image)
#    st.image(Image.open(io.BytesIO(img_data)))
    if uploaded_image:
        try:
            img_data = base64.b64decode(uploaded_image)
            st.image(Image.open(io.BytesIO(img_data)))
        except TypeError:
            st.write("No image uploaded or invalid image format.")



import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from io import BytesIO


# current_dir:현재 경로 저장 , font_path: 폰트경로지정(NanumGothic.ttf)
current_dir = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(current_dir, "..", "fonts", "NanumGothic.ttf")
if not os.path.exists(font_path):
    raise FileNotFoundError(f"폰트 파일을 찾을 수 없습니다: {font_path}")
pdfmetrics.registerFont(TTFont('NanumGothic', font_path))

def remove_asterisks(text):
    return text.replace('**', '')

# create_pdf 함수 직접 추가
def create_pdf(resume_data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    # 기본 스타일에 NanumGothic 폰트 적용
    normal_style = ParagraphStyle(
        name='Normal',
        parent=styles['Normal'],
        fontName='NanumGothic',
        fontSize=12,
        leading=18
    )

    title_style = ParagraphStyle(
        name='Title',
        parent=styles['Title'],
        fontName='NanumGothic',
        fontSize=18,
        spaceAfter=14
    )

    section_title_style = ParagraphStyle(
        name='SectionTitle',
        parent=styles['Heading2'],
        fontName='NanumGothic',
        fontSize=14,
        spaceBefore=10,
        spaceAfter=10
    )

    resume_text_style = ParagraphStyle(
        name='ResumeText',
        parent=styles['Normal'],
        fontName='NanumGothic',
        fontSize=12,
        leading=20  # 줄 간격을 약간 더 넓게 설정
    )

    content = []

    # 이력서 제목
    title = Paragraph(f"{resume_data['name']}의 이력서", title_style)
    content.append(title)
    content.append(Spacer(1, 0.2 * inch))

    # 직무
    jobs = Paragraph(f"직무: {', '.join(resume_data['jobs'])}", normal_style)
    content.append(jobs)
    content.append(Spacer(1, 0.2 * inch))

    # 경력
    experience = Paragraph(f"경력: {resume_data['start_year']} - {resume_data['end_year']}", normal_style)
    content.append(experience)
    content.append(Spacer(1, 0.2 * inch))

    # 연락처
    contact = Paragraph(f"연락처: {resume_data['contact']}", normal_style)
    content.append(contact)
    content.append(Spacer(1, 0.2 * inch))

    # 학력
    education = Paragraph(f"학력: {resume_data['education']}", normal_style)
    content.append(education)
    content.append(Spacer(1, 0.2 * inch))

    # 자격증
    cert = Paragraph(f"자격증: {resume_data['cert']}", normal_style)
    content.append(cert)
    content.append(Spacer(1, 0.2 * inch))

    # URL
    url = Paragraph(f"URL: {resume_data['url']}", normal_style)
    content.append(url)
    content.append(Spacer(1, 0.2 * inch))

    # 회사
    company = Paragraph(f"회사: {resume_data['company']}", normal_style)
    content.append(company)
    content.append(Spacer(1, 0.2 * inch))

    # 경험
    experience = Paragraph(f"경험: {resume_data['experience']}", normal_style)
    content.append(experience)
    content.append(Spacer(1, 0.2 * inch))

    # 기술
    skills = Paragraph(f"기술: {', '.join(resume_data['skills'])}", normal_style)
    content.append(skills)
    content.append(Spacer(1, 0.2 * inch))

    # 기술 수준
    skill_levels = [[Paragraph(f"{skill}", normal_style), Paragraph(f"{level}", normal_style)] for skill, level in resume_data['skill_levels'].items()]
    skill_table = Table(skill_levels, colWidths=[2 * inch, 4 * inch])
    skill_table.setStyle(TableStyle([
       # ('BACKGROUND', (0, 0), (-1, 0), colors.beige),
      #  ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'NanumGothic'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    content.append(skill_table)
    content.append(Spacer(1, 0.2 * inch))

    # 요약
    summary = Paragraph(f"요약: {resume_data['summary']}", normal_style)
    content.append(summary)
    content.append(Spacer(1, 0.2 * inch))

    # AI가 생성한 이력서 텍스트
    resume_text = Paragraph("AI가 생성한 이력서 텍스트:", section_title_style)
    content.append(resume_text)
    content.append(Spacer(1, 0.2 * inch))
    text_object = Paragraph(remove_asterisks(resume_data['resume_text']).replace('\n', '<br/>'), resume_text_style)
    content.append(text_object)

    doc.build(content)
    buffer.seek(0)
    return buffer.getvalue()

# PDF 다운로드 버튼 생성
pdf_data = create_pdf(resume_data)
st.download_button(
    label="PDF 다운로드",
    data=pdf_data,
    file_name=f"{resume_data['name']}_이력서.pdf",
    mime="application/pdf"
    )
st.markdown("---")


# # pdf_download 모듈의 경로 추가
# pdf_download_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../home/pages'))
# sys.path.append(pdf_download_path)
# import pdf_download

# # PDF 다운로드 버튼 생성
# if st.button("PDF 다운로드"):
#     pdf_data = pdf_download.create_pdf(resume_data)
#     st.download_button(
#         label="PDF 다운로드",
#         data=pdf_data,
#         file_name=f"{resume_data['name']}_이력서.pdf",
#         mime="application/pdf"
#     )
