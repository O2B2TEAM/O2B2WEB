import streamlit as st
from auto_wep import \
    download_pdf_and_extract_text  # auto_wep.py에서 필요한 함수 import
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# GPT-4 모델 초기화
llm = ChatOpenAI(api_key="sk-proj-yhsg5NrooNlcqRhn9sjkT3BlbkFJPVlyezvH9aCm3c4LlHeH")

# 프롬프트 템플릿 설정
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a Korean researcher conducting data collection to write a thesis at the university. Proceed in the following order."),
    ("user", "{input}")
])

# 출력 파서 생성 (GPT-4의 출력을 문자열로 파싱)
output_parser = StrOutputParser()

# 프롬프트 템플릿, GPT-4 모델, 출력 파서를 체인으로 연결
chain = prompt | llm | output_parser

# Streamlit 앱의 타이틀 설정
st.title('AI 자료조사 프로그램')

# 텍스트 입력 필드를 설정하여 사용자로부터 조사할 내용을 입력받음
content = st.text_input("조사하고자 하는 주제를 입력 해 주세요", "")

# "검색" 버튼을 설정
if st.button("작성하기"):
    # 버튼이 눌리면 '요약 중입니다...'라는 메시지와 함께 스피너 표시
    with st.spinner('작성 중입니다...'):
        # 검색어를 이용하여 PDF에서 텍스트를 추출
        shortened_query = content  # 일단 입력된 내용을 직접 shortened_query로 사용
        pdf_text = download_pdf_and_extract_text(shortened_query)
        
        # 체인을 호출하여 GPT-4 모델을 사용하고 결과를 요약
        result = chain.invoke({"input": pdf_text})  # 체인에 사용자 입력 대신 PDF에서 추출한 텍스트 전달
        # 요약 결과를 화면에 출력
        st.write(result)

else:
    # 버튼이 눌리지 않으면 빈 문자열 출력 (화면을 깨끗하게 유지)
    st.write("")
