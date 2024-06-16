import os
import tempfile

import streamlit as st
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.retrievers import MultiQueryRetriever
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 환경 변수 로드
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="노세老世",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.header("노세老世 | AI 모의면접", divider='orange')

# 파일 업로드
uploaded_file = st.file_uploader("이력서 파일을 업로드하세요 (PDF)")
st.write("---")

# 업로드 된 파일을 문서로 변환하는 함수
def pdf_to_document(uploaded_file):
    temp_dir = tempfile.TemporaryDirectory()
    temp_filepath = os.path.join(temp_dir.name, uploaded_file.name)
    with open(temp_filepath, "wb") as f:
        f.write(uploaded_file.getvalue())
    loader = PyPDFLoader(temp_filepath)
    pages = loader.load_and_split()
    return pages

if uploaded_file is not None:
    pages = pdf_to_document(uploaded_file)
    # 텍스트 분할
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False,
    )
    texts = text_splitter.split_documents(pages)

    # 임베딩
    embeddings_model = OpenAIEmbeddings(api_key=openai_api_key)

    # Chroma에 로드
    db = Chroma.from_documents(texts, embeddings_model)

    # Conversational Memory
    memory = ConversationBufferMemory(memory_key="chat_history")

    # Chat 모델 설정
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7, api_key=openai_api_key)

    # 질문 생성기용 프롬프트 템플릿
    question_prompt = PromptTemplate.from_template(
        "다음 질문을 생성해주세요. 이력서 내용: {context}, 답변: {answer}"
    )

    # 질문 생성기용 LLM 체인
    question_generator = LLMChain(llm=llm, prompt=question_prompt)

    # 문서 조합용 프롬프트 템플릿
    combine_prompt = PromptTemplate.from_template(
        "문서에서 답변을 조합해주세요: {context}"
    )

    # 문서 조합용 LLM 체인
    combine_docs_chain = StuffDocumentsChain(
        llm_chain=LLMChain(llm=llm, prompt=combine_prompt)
    )

    # Conversational Retrieval QA Chain
    qa_chain = ConversationalRetrievalChain(
        retriever=db.as_retriever(),
        combine_docs_chain=combine_docs_chain,
        question_generator=question_generator,
        memory=memory
    )

    # 초기 질문 설정
    initial_question = "이력서를 바탕으로 기술 면접을 시작합니다. 자기소개를 부탁드립니다."

    # 대화 기록 저장
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "user_answer" not in st.session_state:
        st.session_state.user_answer = ""

    # 챗봇 응답
    def get_bot_response(answer, context):
        response = question_generator({"answer": answer, "context": context})
        return response['text']

    # 초기 질문 응답
    if "initial_question" not in st.session_state:
        st.session_state.initial_question = initial_question
        st.session_state.chat_history.append(("면접관", initial_question))

    for i, (speaker, text) in enumerate(st.session_state.chat_history):
        if speaker == "지원자":
            st.markdown(
                f"<div style='background-color: #FFFCEE; padding: 10px; border-radius: 10px; text-align: right; margin-bottom: 10px;'>{text}</div>", 
                unsafe_allow_html=True
            )
        elif speaker == "면접관":
            st.markdown(
                f"<div style='background-color: #FFFFFF; padding: 10px; border: 2px solid #FF9000; border-radius: 10px; text-align: left; margin-bottom: 10px;'> <strong>면접관:</strong> {text}</div>", 
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div style='background-color: #FFFECE; padding: 10px; border-radius: 10px; border: 1px solid brown; margin-bottom: 10px;'>{text}</div>", 
                unsafe_allow_html=True
            )

    if st.session_state.chat_history and st.session_state.chat_history[-1][0] == "면접관":
        user_answer = st.text_input("답변을 입력하세요:", value=st.session_state.user_answer, key="user_answer_input")
        if st.button('답변 제출'):
            st.session_state.chat_history.append(("지원자", user_answer))
            with st.spinner('챗봇이 다음 질문을 생성 중입니다...'):
                context = " ".join([page.page_content for page in pages])
                next_question = get_bot_response(user_answer, context)
                st.session_state.chat_history.append(("면접관", next_question))
                st.session_state.user_answer = ""  # Clear the input field
                st.experimental_rerun()

    st.write("---")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button('초기화'):
            st.session_state.chat_history = []
            st.session_state.initial_question = initial_question
            st.session_state.chat_history.append(("면접관", initial_question))
            st.session_state.user_answer = ""  # Clear the input field
            st.experimental_rerun()  # Add this line to refresh the page

    with col2:
        if st.button('조언 듣기'):
            user_answer = st.session_state.user_answer
            with st.spinner('조언을 생성 중입니다...'):
                context = " ".join([page.page_content for page in pages])
                feedback_prompt = PromptTemplate.from_template(
                    "지원자의 답변: {answer} 이 답변에 대한 피드백을 제공해주세요. 이력서 내용: {context}"
                )
                feedback_chain = LLMChain(llm=llm, prompt=feedback_prompt)
                feedback = feedback_chain({"answer": user_answer, "context": context})['text']
                st.session_state.chat_history.append(("조언자", feedback))
                st.experimental_rerun()
