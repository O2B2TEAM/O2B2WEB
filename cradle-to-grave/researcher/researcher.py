import os

import requests
import streamlit as st
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# 환경 변수 로드
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="논문 자동 다운로드",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# GPT-4 모델을 호출하는 llm 객체 생성
llm = OpenAI(api_key=openai_api_key)

# 프롬프트 템플릿 설정
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are conducting research to write a paper. Please write a research report."),
    ("user", "{input}")
])

# 체인 설정
llm_chain = LLMChain(prompt=prompt, llm=llm)

# 논문 스크래핑 함수 (예: ArXiv)
def scrape_arxiv_papers(query):
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=5"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'xml')
    entries = soup.find_all('entry')
    papers_list = []
    for entry in entries:
        title = entry.title.text
        pdf_link = entry.find('link', title='pdf')['href']
        summary = entry.summary.text
        papers_list.append({'title': title, 'link': pdf_link, 'summary': summary})
    return papers_list

# 요약을 번역하는 함수
def translate_summary(summary):
    input_text = f"Translate the following summary to Korean:\n{summary}"
    translated_summary = llm_chain.run(input=input_text)
    return translated_summary

st.subheader("노세老世 | 자료조사", divider='orange')
st.markdown("해외 논문 사이트에서 논문을 검색하고 논문 다운로드 링크와 요약의 번역본을 제공합니다.")
st.markdown(" ")

# 검색어 입력
content = st.text_input("검색할 논문의 주제는 무엇인가요?", "")

# "검색 및 다운로드" 버튼을 설정
if st.button("검색 및 다운로드"):
    if not content:
        st.error("검색어를 입력하세요.")
    else:
        with st.spinner('검색 중입니다...'):
            papers_list = scrape_arxiv_papers(content)
            
            if papers_list:
                for paper in papers_list:
                    st.markdown("---")
                    st.markdown(f"### {paper['title']}")
                    st.markdown(f"[PDF 링크]({paper['link']})")
                    translated_summary = translate_summary(paper['summary'])
                    st.markdown(f"서두: {translated_summary}")
            else:
                st.error("논문을 찾을 수 없습니다. 다른 검색어를 시도해 보세요.")
else:
    # 버튼이 눌리지 않으면 빈 문자열 출력 (화면을 깨끗하게 유지)
    st.write("")
