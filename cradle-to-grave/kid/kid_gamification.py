import streamlit as st

st.header("노세노세", divider='orange')

st.subheader("금융 게임")

st.markdown(" ")

col1, col2=st.columns(2)
with col1:
    with st.container():
        st.title("마법의 용돈 모험")
        st.image("images/image1.jpg")
        st.text("game description")
        st.page_link("pages/game_story.py", label="게임 실행하기")
with col2:
    with st.container():
        st.title("another game")
        st.image("images/image2.jpg")
        st.text("게임 설명")
        st.page_link("pages/game2.py", label="게임 실행하기")


