import streamlit as st

st.title('인재 추천 페이지')

# 세션 상태에서 데이터 읽기
jobs = st.session_state.get('jobs', [])
start_year = st.session_state.get('start_year', "신입")
end_year = st.session_state.get('end_year', "15년 이상")
url = st.session_state.get('url', "")

st.markdown("### (값 이동 확인용)입력된 정보:")
st.write(f"선택한 직무: {jobs}")
st.write(f"입사 연차: {start_year}")
st.write(f"퇴사 연차: {end_year}")
st.write(f"채용공고 URL: {url}")

#값을 이용하여 chat gpt로 해당하는 이력서 DB에서 가져오기
st.markdown("**직군 선택하기**") # 별 두 개는 bold

st.markdown("**직군 선택에 따라 인재추천 페이지 불러오기**") # 별 두 개는 bold

st.markdown("**연차+해당 직군 결과 반영된 이력서 선택하기->이력서 보여주는 페이지로 이동**") # 별 두 개는 bold
