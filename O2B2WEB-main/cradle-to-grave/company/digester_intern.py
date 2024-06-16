
import streamlit as st
# OpenAI의 GPT-4 API를 사용하기 위한 라이브러리 임포트
from langchain_openai import ChatOpenAI

# GPT-4 모델을 호출하는 llm 객체 생성
llm = ChatOpenAI()

# 프롬프트 템플릿 설정을 위한 라이브러리 임포트
from langchain_core.prompts import ChatPromptTemplate

# 프롬프트 템플릿 설정
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a world class 'README.md' file writer. Write Markdown file."),  # 시스템 메시지: 모델의 역할 설정
    ("user", "{input}")  # 사용자 메시지: 실제 입력 값을 대체할 변수 포함
])

# 출력 파서를 설정하기 위한 라이브러리 임포트
from langchain_core.output_parsers import StrOutputParser

# 출력 파서 생성 (GPT-4의 출력을 문자열로 파싱)
output_parser = StrOutputParser()

# 프롬프트 템플릿, GPT-4 모델, 출력 파서를 체인으로 연결
chain = prompt | llm | output_parser

# Streamlit UI 구성 요소 임포트
import streamlit as st

# Streamlit 앱의 타이틀 설정
st.title('AI 인턴')

# 텍스트 입력 필드를 설정하여 사용자로부터 조사할 내용을 입력받음
content = st.text_input("코드를 넣어주세요", "")

# "검색" 버튼을 설정
if st.button("작성하기"):
    # 버튼이 눌리면 '요약 중입니다...'라는 메시지와 함께 스피너 표시
    with st.spinner('작성 중입니다...'):
        # 체인을 호출하여 사용자가 입력한 내용을 기반으로 GPT-4 모델을 호출하고 결과를 요약
        result = chain.invoke({"input": content + "이 코드의 README.md 파일을 MardkDown 문법을 이용해서 작성해줘"})
        # 요약 결과를 화면에 출력
        st.write(result)
else:
    # 버튼이 눌리지 않으면 빈 문자열 출력 (화면을 깨끗하게 유지)
    st.write("")
