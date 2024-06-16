import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="노세老世",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.header("노세老世", divider='orange')
st.markdown(''':rainbow[slogan, 노년을 행복하게]''')

col1, col2 =st.columns(2)
with col1: 
    st.header("일자리를 구하고 계신가요?")
    st.markdown("")
    st.markdown("**AIHR**")
    st.markdown("원하는 인재를 AI가 자동으로 추천해드려요")
    st.markdown("**이력서 자동 생성**")
    st.markdown("이력서 작성에 스트레스 받지 마세요. 이력서를 자동으로 생성해드려요")
    st.markdown("**AI 기술면접**")
    st.markdown("나의 이력서로 AI와 모의면접을 진행해요")
with col2:    
    st.image("images/sundayafternoon.jpg")

st.markdown(''':rainbow[From cradle to grave service]''')
col1,col2,col3,col4,col5= st.columns(5)
with col1:
    st.header("어린이")
    st.markdown('''금융교육''')
with col2:
    st.header("노인")
    st.markdown('''노인복지 현황 데이터 보고''')
with col3:
    st.header("연구소")
    st.markdown('''자료조사''')
with col4:
    st.header("기업")
    st.markdown('''데일리 리포트''')
with col5:
    st.header("군인")
    st.markdown('''군인복지''')

st.markdown("""---""")

col1, col2 =st. columns(2)
with col1:
    st.text("join with us")
with col2:
    st.text("have you ever login?")

col1, col2 =st. columns(2)
with col1: 
    st.page_link("pages/join.py", label="회원가입")
with col2:
    st.page_link("pages/login.py", label="로그인")