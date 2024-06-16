import streamlit as st

# 제목과 설명 추가
st.title('채용하고 싶은 인재 조건이 있으신가요?')
st.markdown("")

st.markdown("**직무를 선택해주세요**") # 별 두 개는 bold

# Jobs 입력 받기 (여러 개 선택 가능)
jobs = st.multiselect(
    "직무를 선택해주세요.",
    ["DevOps/시스템 관리자", "HW/임베디드 개발자", "IOS 개발자",
     "데이터 사이언티스트", "데이터 엔지니어", "서버/백엔드 개발자",
     "안드로이드 개발자", "프론트엔드 개발자", "게임 서버 개발자",
     "게임 클라이언트 개발자"])

st.write("선택한 직무:", jobs)

# start_year 입력 받기, end_year 입력 받기
start_year, end_year = st.select_slider(
    "연차를 선택해주세요",
    options=["신입", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15년 이상"],
    value=("신입", "15년 이상"))

st.write("입사 연차:", start_year)
st.write("퇴사 연차:", end_year)

# URL 입력 받기
url = st.text_input("채용공고 URL을 입력해주세요")

st.write("URL:", url)

# 상태 저장
if 'jobs' not in st.session_state:
    st.session_state.jobs = []
if 'start_year' not in st.session_state:
    st.session_state.start_year = ""
if 'end_year' not in st.session_state:
    st.session_state.end_year = ""
if 'url' not in st.session_state:
    st.session_state.url = ""

st.session_state.jobs = jobs
st.session_state.start_year = start_year
st.session_state.end_year = end_year
st.session_state.url = url

# 페이지 이동 버튼
st.page_link("pages/page_2.py", label="인재 추천 받기")

# 확인용 결과창
if st.button('결과 출력'):
    st.markdown("### 결과:")
    st.write(f"jobs: {st.session_state.jobs}")
    st.write(f"start_year: {st.session_state.start_year}")
    st.write(f"end_year: {st.session_state.end_year}")
    st.write(f"url: {st.session_state.url}")