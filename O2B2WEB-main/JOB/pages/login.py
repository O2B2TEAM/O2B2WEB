import streamlit as st

# 제목
st.title('로그인 화면')
st.markdown("")

id = st.text_input("아이디")
st.write("id:", id)

pw = st.text_input("비밀번호")
st.write("password:", pw)

# 상태 저장->DB로 변환
if 'name' not in st.session_state:
    st.session_state.name = ""
if 'id' not in st.session_state:
    st.session_state.id = ""
if 'pw' not in st.session_state:
    st.session_state.pw = ""

st.session_state.name = name
st.session_state.id = id
st.session_state.pw=pw

# 페이지 이동 버튼
st.page_link("join.py", label="회원가입 완료(click,페이지이동)")

# 확인용 결과창
if st.button('결과 출력'):
    st.markdown("### 결과:")
    st.write(f"이름: {st.session_state.name}")
    st.write(f"ID: {st.session_state.id}")
    st.write(f"password: {st.session_state.pw}")