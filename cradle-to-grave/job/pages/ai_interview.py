import os
import tempfile

import streamlit as st
#챗봇
from langchain.chains import RetrievalQA
# import question
from langchain.retrievers.multi_query import MultiQueryRetriever
# import
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.embeddings.sentence_transformer import \
    SentenceTransformerEmbeddings
from langchain_openai import ChatOpenAI
from langchain_text_splitters import (CharacterTextSplitter,
                                      RecursiveCharacterTextSplitter)

#제목
st.header("AI 인터뷰", divider='orange')
st.markdown(" ")

#파일 업로드
uploaded_file = st.file_uploader("자소서 pdf 파일을 넣어 주세요.")
st.write("---")

def configure_retriever(uploaded_file):
    # Read documents
    docs = []
    temp_dir = tempfile.TemporaryDirectory()
    # 업로드된 파일을 직접 읽을 수 있도록 루프를 수정합니다.
    temp_filepath = os.path.join(temp_dir.name, uploaded_file.name)
    with open(temp_filepath, "wb") as f:
        f.write(uploaded_file.read())
    
    loader = PyPDFLoader(temp_filepath)
    pages = loader.load_and_split()
    
    return pages

# Splitter 초기화
text_splitter = RecursiveCharacterTextSplitter()  # 또는 CharacterTextSplitter()

if uploaded_file is not None:
    pages = configure_retriever(uploaded_file)
    texts = text_splitter.split_documents(pages)

    # Embedding DB에 저장할 수 있는 형태로 변환
    from langchain_openai import OpenAIEmbeddings
    embeddings_model = OpenAIEmbeddings()

    # load it into Chroma
    db = Chroma.from_documents(texts, embeddings_model)

    # Question
    st.header("PDF에게 질문해보세요")
    question = st.text_input("질문을 입력하세요")


    if st.button('질문하기'):
        llm = ChatOpenAI(api_key="sk-proj-yhsg5NrooNlcqRhn9sjkT3BlbkFJPVlyezvH9aCm3c4LlHeH")
        qa_chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())
        result = qa_chain.invoke({"query": question+"에 대해 한글로"})
        
        # 출력 형식을 원하는 형태로 변경
        st.write(result['result'])
