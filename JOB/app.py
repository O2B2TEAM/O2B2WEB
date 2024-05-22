import streamlit as st

import time

with st.spinner('페이지를 생성 중입니다...'):
    time.sleep(5)

#회사소개
st.markdown("**회사를 소개합니다**") # 별 두 개는 
st.page_link("app.py", label="Home", icon="🏠")
st.page_link("pages/page_1.py", label="AIHR")
st.page_link("pages/page_2.py", label="AIHR(추후삭제)")
st.page_link("pages/page_3.py", label="이력서 생성")
st.page_link("pages/page_4.py", label="이력서 생성(추후삭제)")
st.page_link("pages/join.py", label="회원가입")
st.page_link("pages/page_6.py", label="회원가입완료(추후삭제)")
st.page_link("pages/login.py", label="로그인")
st.page_link("pages/page_6.py", label="회원가입완료(추후삭제)")

#회원가입
# 페이지 이동 버튼
st.page_link("pages/join.py", label="회원가입")

st.markdown("**이미 계정이 있으신가요?**") # 별 두 개는 
#로그인
st.page_link("login.py", label="회원가입")






