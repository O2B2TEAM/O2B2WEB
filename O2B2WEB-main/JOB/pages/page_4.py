import streamlit as st



st.title('')

# 세션 상태에서 데이터 읽기

start_year = st.session_state.get('start_year', "신입")
end_year = st.session_state.get('end_year', "15년 이상")
company = st.session_state.get('company', "")
jobs = st.session_state.get('jobs', [])
url = st.session_state.get('url', "")

st.markdown("### (값 이동 확인용)입력된 정보:")

st.write(f"입사 연차: {start_year}")
st.write(f"퇴사 연차: {end_year}")
st.write(f"직장명: {company}")
st.write(f"선택한 직무: {jobs}")
st.write(f"역량 소개: {url}")

#값을 이용하여 이력서 생성하기
#ai 로 코드생성


