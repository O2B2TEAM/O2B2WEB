import streamlit as st

st.title('회원가입 완료 페이지')

# 세션 상태에서 데이터 읽기
name = st.session_state.get('name', "")
id = st.session_state.get('id', "")
pw = st.session_state.get('pw', "")

st.markdown("### (값 이동 확인용)입력된 정보:")
st.write(f"이름: {name}")
st.write(f"ID: {id}")
st.write(f"password: {pw}")