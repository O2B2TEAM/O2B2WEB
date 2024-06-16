# pages/pdf_download.py
import tempfile

#import pdfkit
import streamlit as st
from pymongo import MongoClient

st.set_page_config(
    page_title="노세老世",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# wkhtmltopdf 실행 파일 경로 설정
#path_to_wkhtmltopdf = 'C:/Program Files (x86)/wkhtmltopdf/bin/wkhtmltopdf.exe'  #wkhtmltopdf.exe 파일 경로
#config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

# MongoDB Atlas 클라이언트 설정
client = MongoClient("mongodb+srv://test:1234@cluster.ct8weib.mongodb.net/o2b2data?retryWrites=true&w=majority")
db = client["o2b2data"]
resume_collection = db["resume_user"]

# 로그인 상태 확인
if 'logged_in' in st.session_state and st.session_state.logged_in:
    user_name = st.session_state.user_data.get('name')

    # 사용자 이름과 일치하는 이력서 정보 가져오기
    resume_data = resume_collection.find_one({"name": user_name})

    if resume_data:
        st.title("PDF 다운로드")
        
        # 이력서 HTML 템플릿 생성
        resume_html = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; }}
                h1 {{ color: #333; }}
                p {{ margin: 0; }}
                .section {{ margin-bottom: 20px; }}
            </style>
        </head>
        <body>
            <h1>{resume_data['name']}의 이력서</h1>
            <div class="section">
                <h2>직무</h2>
                <p>{', '.join(resume_data['jobs'])}</p>
            </div>
            <div class="section">
                <h2>경력</h2>
                <p>시작 연도: {resume_data['start_year']}</p>
                <p>종료 연도: {resume_data['end_year']}</p>
            </div>
            <div class="section">
                <h2>연락처</h2>
                <p>{resume_data['contact']}</p>
            </div>
            <div class="section">
                <h2>학력</h2>
                <p>{resume_data['education']}</p>
            </div>
            <div class="section">
                <h2>자격증</h2>
                <p>{resume_data['cert']}</p>
            </div>
            <div class="section">
                <h2>URL</h2>
                <p>{resume_data['url']}</p>
            </div>
            <div class="section">
                <h2>회사</h2>
                <p>{resume_data['company']}</p>
            </div>
            <div class="section">
                <h2>경험</h2>
                <p>{resume_data['experience']}</p>
            </div>
            <div class="section">
                <h2>기술</h2>
                <p>{', '.join(resume_data['skills'])}</p>
            </div>
            <div class="section">
                <h2>기술 수준</h2>
                <ul>
                    {''.join([f"<li>{skill}: {level}</li>" for skill, level in resume_data['skill_levels'].items()])}
                </ul>
            </div>
            <div class="section">
                <h2>요약</h2>
                <p>{resume_data['summary']}</p>
            </div>
            <div class="section">
                <h2>AI가 생성한 이력서 텍스트</h2>
                <p>{resume_data['resume_text']}</p>
            </div>
        </body>
        </html>
        """

        # 임시 파일에 PDF 생성
  #      with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
   #         pdfkit.from_string(resume_html, tmpfile.name, configuration=config)
   #         tmpfile.seek(0)
   #         pdf_data = tmpfile.read()

        # PDF 다운로드 버튼
        st.download_button(
            label="PDF 다운로드",
            data=pdf_data,
            file_name=f"{resume_data['name']}_이력서.pdf",
            mime="application/pdf"
        )
    else:
        st.error("이력서 정보를 찾을 수 없습니다.")
else:
    st.error("로그인이 필요합니다. 로그인 해주세요.")
    st.page_link("pages/login.py", label="로그인 페이지로 이동")