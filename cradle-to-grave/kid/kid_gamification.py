import streamlit as st

st.set_page_config(
    page_title="노세老世",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.header("노세老世 | 두뇌개발", divider='orange')
st.markdown(":green[두뇌개발] & :red[머리식히기]")
st.markdown(" ")

col1, col2=st.columns(2)
with col1:
    with st.container(border=True):
        st.subheader("마법 용돈 모험")
        st.image("images/image1.jpg")
        st.markdown("게이미피케이션을 통한 경제 학습")
        st.markdown("---")
        st.page_link("pages/game_story.py", label="게임 하러 가기")
with col2:
    with st.container(border=True):
        st.subheader("한국 전통 카드 게임")
        st.image("images/gostop.jpg")
        st.markdown("게임을 통해 구직 스트레스를 즐겁게 날려보세요")
        st.markdown("---")
        st.page_link("pages/game2.py", label="게임 하러 가기")


