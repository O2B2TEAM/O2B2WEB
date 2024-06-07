import streamlit as st

# Initialize session state variables
if 'health' not in st.session_state:
    st.session_state.health = 100
if 'gold' not in st.session_state:
    st.session_state.gold = 0
if 'step' not in st.session_state:
    st.session_state.step = 1

# Function to reset the game
def reset_game():
    st.session_state.health = 100
    st.session_state.gold = 0
    st.session_state.step = 1

# Function to handle choice and update state
def handle_choice(choice):
    if st.session_state.step == 1:
        if choice == 'a':
            st.session_state.gold += 5
        elif choice == 'b':
            st.session_state.gold += 2.5
        st.session_state.step += 1

    elif st.session_state.step == 2:
        if choice == 'a':
            st.session_state.gold -= 5
        elif choice == 'b':
            st.session_state.gold -= 10
        st.session_state.step += 1

    elif st.session_state.step == 3:
        if choice == 'a':
            st.session_state.health -= 10
            st.session_state.gold += 2
        elif choice == 'b':
            st.session_state.health -= 30
            st.session_state.gold += 5
        st.session_state.step += 1

    elif st.session_state.step == 4:
        if choice == 'a':
            st.session_state.gold -= 15
        elif choice == 'b':
            st.session_state.gold -= 15  # Assuming borrowing logic is handled separately
        st.session_state.step += 1

    elif st.session_state.step == 5:
        if choice == 'a':
            st.session_state.health = 100
            st.session_state.gold -= 5
        elif choice == 'b':
            st.session_state.health += 20
            st.session_state.gold -= 2
        st.session_state.step += 1

    elif st.session_state.step == 6:
        if choice == 'a':
            st.session_state.gold -= 2
        elif choice == 'b':
            st.session_state.gold -= 5
        st.session_state.step += 1

# Game steps and choices
steps = {
    1: {
        'subheader':"첫 번째 황금 코인",
        'image': "images/image1.jpg",
        'text': "부모님이 첫 번째로 황금 코인 5개를 주셨어요. 이 코인으로 마법의 물건을 살 수 있어요. 부모님은 '황금 코인을 잘 관리하는 것은 중요한 기술이야. 어떻게 사용할지 신중하게 생각해보렴.'이라고 말씀하셨습니다.",
        'choices': {
            'a': "모두 저축하기 (마법의 은행에 보관)",
            'b': "절반 저축하고 절반 사용하기",
            'c': "모두 사용하기"
        }
    },
    2: {
        'subheader':"요정 친구의 생일 파티",
        'image': "images/image3.jpg",
        'text': "요정 친구 루미의 생일 파티에 초대받았어요. 루미는 항상 당신에게 친절하게 대해주었어요. 루미에게 멋진 선물을 주고 싶어요.",
        'choices': {
            'a': "5개 코인짜리 작은 마법 선물 사기",
            'b': "10개 코인짜리 큰 마법 선물 사기",
            'c': "직접 만든 마법 선물 주기 (비용 없음)"
        }
    },
    3: {
        'subheader':"마법의 숲 모험",
        'image': "images/image4.jpg",
        'text': "당신은 마법의 숲으로 모험을 떠나기로 했어요. 이 숲은 아름다운 경치와 신비한 생물들로 가득하지만, 위험도 도사리고 있어요. 친구들은 안전한 경로를 따라가자고 하지만, 당신은 더 깊이 들어가고 싶어요.",
        'choices': {
            'a': "안전한 경로를 따라 탐험하기",
            'b': "위험한 경로를 따라 더 깊이 탐험하기",
            'c': "모험을 포기하고 집에 있기"
        }
    },
    4: {
        'subheader':"큰 지출 결심",
        'image': "images/image5.jpg",
        'text': "사고 싶은 마법 장난감이 있어요. 가격은 15개 코인입니다. 이 장난감은 당신이 꿈꾸던 아이템이지만, 현재 모은 돈으로는 살 수 없어요.",
        'choices': {
            'a': "지금까지 모은 돈으로 사기",
            'b': "부모님께 돈을 빌려서 사기",
            'c': "더 모을 때까지 기다리기"
        }
    },
    5: {
        'subheader':"마법 치료",
        'image': "images/image6.jpg",
        'text': "모험을 통해 Health가 감소했습니다. 회복을 위해 마법 치료를 받을 수 있어요. 마법 치료사는 '건강은 돈보다 더 소중한 것이에요. 잘 관리해야 한답니다.'라고 말합니다.",
        'choices': {
            'a': "5개 코인을 사용하여 완전 회복하기",
            'b': "2개 코인을 사용하여 부분 회복하기",
            'c': "치료를 받지 않고 회복 기다리기"
        }
    },
    6: {
        'subheader':"돈을 기부하기",
        'image': "images/image7.png",
        'text': "마법 학교에서 어려운 친구들을 돕기 위한 모금 행사를 열어요. 마법 선생님은 '기부는 자신을 나누는 일이란다. 함께 도와 어려운 친구들에게 희망을 주자.'라고 말합니다.",
        'choices': {
            'a': "2개 코인 기부하기",
            'b': "5개 코인 기부하기",
            'c': "기부하지 않기"
        }
    }
}
st.header("마법 용돈 모험: 황금 코인의 비밀과 건강의 지혜", divider='orange')
# Main game logic
if st.session_state.step <= len(steps):
    step = steps[st.session_state.step]
    st.subheader(step['subheader'])
    st.markdown(" ")
    col1, col2=st.columns(2)
    with col1:
        st.image(step['image'])
    with col2:
        with st.container(height=200):
            st.markdown(step['text'])
    st.markdown("""---""")
    col1, col2 = st.columns(2)
    with col1:
        st.text("Q. 어떤 선택을 하시겠어요?")
        st.markdown(" ")
        st.write(f"	:heartbeat:{st.session_state.health}")
        st.write(f"	:coin:{st.session_state.gold}")
    with col2:
        for choice_key, choice_text in step['choices'].items():
            if st.button(choice_text, key=choice_key):
                handle_choice(choice_key)



else:
    st.subheader("게임이 끝났습니다!")
    st.image("images/image8.jpg")
    st.subheader(f" 당신의 최종 :heartbeat:{st.session_state.health}")
    st.subheader(f" 당신의 최종 :coin:{st.session_state.gold}")
    st.markdown(" ")
    if st.button("다시 시작하기"):
        reset_game()


