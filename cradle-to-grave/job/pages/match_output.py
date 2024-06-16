import base64
import io
import smtplib
from email.mime.text import MIMEText

import streamlit as st
from PIL import Image
from pymongo import MongoClient

st.set_page_config(
    page_title="노세老世",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 필요한 세션 상태 변수 초기화
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None
if 'jobs' not in st.session_state:
    st.session_state.jobs = []
if 'start_year' not in st.session_state:
    st.session_state.start_year = "신입"
if 'end_year' not in st.session_state:
    st.session_state.end_year = "15년 이상"
if 'result' not in st.session_state:
    st.session_state.result = ""

    # MongoDB 클라이언트 생성
client = MongoClient("mongodb+srv://test:1234@cluster.ct8weib.mongodb.net/o2b2data?retryWrites=true&w=majority")
db = client["o2b2data"]
collection = db["resume_user"]

# Streamlit 애플리케이션 구성
st.header("노세老世 | AI HR", divider='orange')
st.subheader("인재 추천 결과")
st.markdown(" ")

# 세션 상태에서 데이터 읽기
jobs = st.session_state.get('jobs', [])
start_year = st.session_state.get('start_year', "신입")
end_year = st.session_state.get('end_year', "15년 이상")

# end_year를 숫자로 변환
end_year_map = {
    "신입": 0,
    "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
    "7": 7, "8": 8, "9": 9, "10": 10, "11": 11, "12": 12,
    "13": 13, "14": 14, "15년 이상": 15
}
end_year_numeric = end_year_map.get(end_year, 15)

col1,col2=st.columns(2)
with col1:
    st.markdown(f"**채용 분야: {jobs}**")
with col2:
    st.markdown(f"**경력: {end_year}**")
st.markdown("---")

# 필터링 조건에 맞는 이력서를 MongoDB에서 가져오기
query = {
    "jobs": {"$in": jobs},
    "start_year": start_year,  # "신입"과 같은 문자열로 직접 비교
    "end_year": {"$gte": end_year_numeric}  # 숫자로 변환된 end_year와 비교
}

results = list(collection.find(query))  # Cursor 객체를 리스트로 변환
num_results = len(results)  # 필터링된 결과의 개수

# 필터링된 이력서 결과 출력
if len(results) > 0:
    st.markdown(f"##### 총 {num_results}건의 이력서가 매칭되었습니다. #####")
    displayed_ids = set()  # 중복 출력을 방지하기 위한 ID 집합


    for result in results:
        if result['_id'] not in displayed_ids:
            displayed_ids.add(result['_id'])
            with st.expander(f"{result['name']} - {', '.join(result['jobs'])} - 경력: {result['start_year']} - {result['end_year']}"):
                st.write(f"이름: {result['name']}")
                st.write(f"직무: {', '.join(result['jobs'])}")
                st.write(f"경력: {result['start_year']} - {result['end_year']}")
                st.write(f"연락처: {result.get('contact', '정보가 없습니다.')}")
                st.write(f"학력: {result.get('education', '정보가 없습니다.')}")
                st.write(f"자격증: {result.get('cert', '정보가 없습니다.')}")
                st.write(f"URL: {result.get('url', '정보가 없습니다.')}")
                st.write(f"회사: {result.get('company', '정보가 없습니다.')}")
                st.write(f"경력: {result.get('experience', '정보가 없습니다.')}")
                st.write(f"기술: {', '.join(result['skills'])}")
                st.write(f"기술 레벨: {result['skill_levels']}")
                st.write(f"자기소개: {result['summary']}")
                st.write(f"이력서 내용: {result['resume_text']}")
                
                if st.button(f"연락 보내기", key=result['_id']):
                    with st.form(key=f"form_{result['_id']}"):
                        company_name = st.text_input("회사 이름")
                        contact_info = st.text_input("연락처")
                        message = st.text_area("메세지")
                        submit_button = st.form_submit_button(label="보내기")

                        if submit_button:
                            collection.update_one(
                                {"_id": result['_id']},
                                {"$set": {"employ": True, "company_name": company_name, "company_contact": contact_info, "message": message}}
                            )
                            st.success("채용 연락을 보냈습니다.")

else:
    st.write("해당 조건에 맞는 인재를 찾을 수 없습니다.")

