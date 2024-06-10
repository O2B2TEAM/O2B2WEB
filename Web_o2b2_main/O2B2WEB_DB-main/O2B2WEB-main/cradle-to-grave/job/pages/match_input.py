import streamlit as st

# 필요한 세션 상태 변수 초기화
if 'jobs' not in st.session_state:
    st.session_state.jobs = []
if 'start_year' not in st.session_state:
    st.session_state.start_year = "신입"
if 'end_year' not in st.session_state:
    st.session_state.end_year = "15년 이상"
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None
if 'result' not in st.session_state:
    st.session_state.result = ""

# Streamlit 애플리케이션 구성
st.header("노세노세 | AI HR", divider='orange')
st.subheader("인재추천")
st.markdown(" ")

# 직무 선택 옵션 정의
jobs_options = ["DevOps/시스템 관리자", "HW/임베디드 개발자", "IOS 개발자",
                "데이터 사이언티스트", "데이터 엔지니어", "서버/백엔드 개발자",
                "안드로이드 개발자", "프론트엔드 개발자", "게임 서버 개발자",
                "게임 클라이언트 개발자"]

# UI 레이아웃 설정
col1, col2 = st.columns([2, 2])

with col1:
    jobs = st.multiselect(
        "채용하고 싶은 직무를 입력 해 주세요.",
        jobs_options
    )

with col2:
    start_year, end_year = st.select_slider(
        "채용하고 싶은 연차를 선택해주세요",
        options=["신입", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15년 이상"],
        value=("신입", "15년 이상")
    )

# 세션 상태에 입력 데이터 저장
st.session_state.jobs = jobs
st.session_state.start_year = start_year
st.session_state.end_year = end_year

# 페이지 이동 버튼
st.page_link("pages/match_output.py", label="인재 추천 받기")

# 결과 출력 버튼
if st.button('결과 출력'):
    st.markdown("### 결과:")
    st.write(f"선택한 직무: {st.session_state.jobs}")
    st.write(f"입사 연차: {st.session_state.start_year}")
    st.write(f"퇴사 연차: {st.session_state.end_year}")

st.markdown("---")
