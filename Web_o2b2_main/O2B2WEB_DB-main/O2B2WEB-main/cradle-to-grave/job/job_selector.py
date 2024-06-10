import streamlit as st
import streamlit.components.v1 as components

st.header("노세노세", divider='orange')
st.subheader("AI HR")
st.markdown(" ")

col1,col2,col3= st.columns(3)
with col1:
    with st.container():
        st.subheader("구직자") 
        st.markdown("AI 기반 이력서를 작성 해 드려요.")
        st.page_link("pages/resume_make.py", label="이력서 생성하기") 
        
with col2:
    with st.container():
        st.subheader("고용인") 
        st.markdown("AI 기반 고용 시스템을 사용 해 보시겠어요?")
        st.page_link("pages/match_input.py", label="인재 추천받기") 

with col3:
    with st.container():
        st.subheader("인터뷰")
        st.markdown("AI와 모의 기술 면접을 진행합니다.")
        st.page_link("pages/ai_interview.py", label="모의면접") 