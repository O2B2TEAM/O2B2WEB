import io

import streamlit as st
from PIL import Image

# 제목과 설명 추가
st.title('경력사항을 입력해주세요')
st.markdown("---")

# start_year 입력 받기, end_year 입력 받기
start_year, end_year = st.select_slider(
    "근무기간",
    options=["신입", "1년", "2년", "3년", "4년", "5년", "6년", "7년", "8년", "9년", "10년", "11년", "12년", "13년", "14년", "15년 이상"],
    value=("신입", "15년 이상"))
col1,col2=st.columns(2)
with col1:
    st.write("입사 연차:", start_year)
with col2:
    st.write("퇴사 연차:", end_year)

st.markdown("---")


col1,col2,col3=st.columns(3)
with col1:
    st.header("이미지 업로더")

# 사용자가 여러 파일을 업로드할 수 있도록 허용
    uploaded_files = st.file_uploader("이미지 파일을 선택하세요", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

    for uploaded_file in uploaded_files:
        # 파일을 바이트로 읽기
        bytes_data = uploaded_file.read()

        # PIL을 사용하여 이미지 로드
        image = Image.open(io.BytesIO(bytes_data))

        # 이미지를 103x132 픽셀로 크기 조정
        resized_image = image.resize((103, 132))

        # 파일 이름 표시
        st.image(resized_image)

    
        

with col2:
    name = st.text_input("이름")
    contact = st.text_input("연락처")
    summary = st.text_area("자기소개")
    education = st.text_area("학력")
with col3:
    experience = st.text_area("경력")
    skills = st.text_area("기술")
    cert=st.text_area("자격증")


# 직장명 입력 받기
company = st.text_input("직장명")

# Jobs 입력 받기 (여러 개 선택 가능)
jobs = st.multiselect(
    "직무",
    ["DevOps/시스템 관리자", "HW/임베디드 개발자", "IOS 개발자",
     "데이터 사이언티스트", "데이터 엔지니어", "서버/백엔드 개발자",
     "안드로이드 개발자", "프론트엔드 개발자", "게임 서버 개발자",
     "게임 클라이언트 개발자"])

# URL 입력 받기
url = st.text_input("나의 역량이 잘 나타날 수 있는 url을 입력해주세요")

st.write("URL:", url)


# 상태 저장
if 'company' not in st.session_state:
    st.session_state.company = ""
if 'start_year' not in st.session_state:
    st.session_state.start_year = ""
if 'end_year' not in st.session_state:
    st.session_state.end_year = ""
if 'jobs' not in st.session_state:
    st.session_state.jobs = []
if 'url' not in st.session_state:
    st.session_state.url = ""
if 'name' not in st.session_state:
    st.session_state.name = ""
if 'contact' not in st.session_state:
    st.session_state.contact = ""
if 'summary' not in st.session_state:
    st.session_state.summary = ""
if 'experience' not in st.session_state:
    st.session_state.experience = ""
if 'education' not in st.session_state:
    st.session_state.education = ""
if 'skills' not in st.session_state:
    st.session_state.skills = ""

st.session_state.start_year = start_year
st.session_state.end_year = end_year
st.session_state.company = company
st.session_state.jobs = jobs
st.session_state.url = url
st.session_state.name = name
st.session_state.contact = contact
st.session_state.summary = summary
st.session_state.experience = experience
st.session_state.education = education
st.session_state.skills = skills

# 페이지 이동 버튼
st.text("이력서 생성하기")

# 확인용 결과창
if st.button('결과 출력'):
    st.markdown("### 결과:")
    st.write(f"start_year: {st.session_state.start_year}")
    st.write(f"end_year: {st.session_state.end_year}")
    st.write(f"company: {st.session_state.company}")
    st.write(f"jobs: {st.session_state.jobs}")
    st.write(f"url: {st.session_state.url}")
    st.write(f"name: {st.session_state.name}")
    st.write(f"contact: {st.session_state.contact}")
    st.write(f"summary: {st.session_state.summary}")
    st.write(f"experience: {st.session_state.experience}")
    st.write(f"education: {st.session_state.education}")
    st.write(f"skills: {st.session_state.skills}")

st.markdown("---")