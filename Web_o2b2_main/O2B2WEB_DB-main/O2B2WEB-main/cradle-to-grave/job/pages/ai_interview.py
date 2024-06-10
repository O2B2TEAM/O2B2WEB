import os
import tempfile

import streamlit as st
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pymongo import MongoClient

# 환경 변수 로드
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# MongoDB 클라이언트 생성
client = MongoClient("mongodb+srv://test:1234@cluster.ct8weib.mongodb.net/o2b2data?retryWrites=true&w=majority")
db = client["o2b2data"]
collection = db["aiform_user"]

# 제목
st.header("AI 인터뷰")
st.markdown(" ")

# 사용자가 입력한 이름과 연락처로 해당 사용자의 데이터를 검색
name = st.text_input("이름을 입력하세요")
contact = st.text_input("연락처를 입력하세요")

if st.button('불러오기'):
    user_data = collection.find_one({"name": name, "contact": contact})
    if user_data:
        st.write("### 불러온 데이터:")
        st.write(f"이름: {user_data['name']}")
        st.write(f"연락처: {user_data['contact']}")
        st.write(f"경력: {user_data['experience']}")
        st.write(f"기술: {user_data['skills']}")
        st.write(f"자기소개: {user_data['summary']}")
        st.write("---")

        # PDF 파일 업로드
        uploaded_file = st.file_uploader("자소서 PDF 파일을 넣어 주세요.")
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
        text_splitter = RecursiveCharacterTextSplitter()

        if uploaded_file is not None:
            pages = configure_retriever(uploaded_file)
            texts = text_splitter.split_documents(pages)

            # Embedding DB에 저장할 수 있는 형태로 변환
            embeddings_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

            # load it into Chroma
            db = Chroma.from_documents(texts, embeddings_model)

            # Question
            st.header("PDF에게 질문해보세요")
            question = st.text_input("질문을 입력하세요")

            if st.button('질문하기'):
                llm = ChatOpenAI(api_key=openai_api_key)
                qa_chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())
                result = qa_chain.invoke({"query": question + "에 대해 한글로"})
                
                # 출력 형식을 원하는 형태로 변경
                st.write(result['result'])
    else:
        st.write("사용자 데이터를 찾을 수 없습니다.")
