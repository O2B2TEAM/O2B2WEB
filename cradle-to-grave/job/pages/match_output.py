import base64
import io

import streamlit as st
from PIL import Image

# Streamlit 애플리케이션 구성
st.header("노세老世 | AI HR", divider='orange')
st.subheader("인재추천")
st.markdown(" ")

# 세션 상태에서 데이터 읽기
jobs = st.session_state.get('jobs', [])
start_year = st.session_state.get('start_year', "신입")
end_year = st.session_state.get('end_year', "15년 이상")

col1, col4 = st.columns([3, 1])
with col1:
    st.subheader(f"채용 분야 - {jobs}")
    st.subheader(f"경력: {start_year} - {end_year}")

with col4:
    if st.session_state.uploaded_image:
        img_data = base64.b64decode(st.session_state.uploaded_image)
        st.image(Image.open(io.BytesIO(img_data)))

st.markdown("---")

# 사용자 이력서 결과 보기
if st.session_state.result:
    st.markdown("### 인재 추천 결과:")
    st.write(st.session_state.result)


