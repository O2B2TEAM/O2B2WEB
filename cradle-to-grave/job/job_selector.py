import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="노세老世",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.header("노세老世", divider='orange')
st.subheader("AI HR")
st.markdown(" ")

col1,col2,col3= st.columns(3)
with col1:
    with st.container(border=True):
        st.subheader("구직자") 
        st.image("images/resume.png")
        st.markdown("AI 기반 이력서를 작성 해 드려요.")
        st.markdown("---")
        st.page_link("pages/resume_make.py", label="이력서 생성하기") 
        
with col2:
    with st.container(border=True):
        st.subheader("고용인") 
        st.image("images/system.png")
        st.markdown("AI 기반 고용 시스템을 사용 해 보시겠어요?")
        st.markdown("---")
        st.page_link("pages/match_input.py", label="인재 추천받기") 

with col3:
    with st.container(border=True):
        st.subheader("인터뷰")
        st.image("images/interview.png")
        st.markdown("AI와 모의 면접을 진행합니다.")
        st.markdown("---")
        st.page_link("pages/ai_interview.py", label="모의면접 하러가기") 