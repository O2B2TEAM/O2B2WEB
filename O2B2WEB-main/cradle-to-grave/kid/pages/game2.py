import streamlit as st

# Initialize session state
if 'health' not in st.session_state:
    st.session_state.health = 100
if 'gold' not in st.session_state:
    st.session_state.gold = 5
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0


st.header("마법 용돈 모험: 황금 코인의 비밀과 건강의 지혜", divider='orange')
st.subheader("첫 번째 황금 코인")
st.markdown(" ")

col1, col2 =st.columns(2)
with col1:
    st.image("images/sundayafternoon.jpg")
with col2:
    with st.container(height=200):
        st.markdown("부모님이 첫 번째로 황금 코인 5개를 주셨어요. 이 코인으로 마법의 물건을 살 수 있어요. 부모님은 '황금 코인을 잘 관리하는 것은 중요한 기술이야. 어떻게 사용할지 신중하게 생각해보렴.'이라고 말씀하셨습니다.")


# Game logic
def check_answer(question, selected_option):
    if selected_option == question["answer"]:
        st.session_state.gold += 10
        return True
    else:
        st.session_state.health -= 10
        return False


# Quiz questions and answers
questions = [
    {"question": "What is the capital of France?", "options": ["Berlin", "London", "Paris", "Rome"], "answer": "Paris"},
    {"question": "What does ROI stand for?", "options": ["Return on Investment", "Rate of Interest", "Revenue on Investment", "Return on Income"], "answer": "Return on Investment"},
    {"question": "Which is the largest stock exchange in the world?", "options": ["NASDAQ", "Tokyo Stock Exchange", "London Stock Exchange", "New York Stock Exchange"], "answer": "New York Stock Exchange"},
]


# Display current question
if st.session_state.question_index < len(questions):
    current_question = questions[st.session_state.question_index]

    st.write(f"Health: {st.session_state.health}")
    st.write(f"Gold: {st.session_state.gold}")

    st.header(current_question["question"])

    selected_option = st.radio("Options", current_question["options"])

    if st.button("Submit"):
        if check_answer(current_question, selected_option):
            st.success("Correct!")
            st.session_state.question_index += 1
        else:
            st.error("Incorrect!")
        
        if st.session_state.question_index >= len(questions):
            st.write("You have completed the quiz!")
else:
    st.write("Game Over!")
    st.write(f"Final Health: {st.session_state.health}")
    st.write(f"Final Gold: {st.session_state.gold}")
