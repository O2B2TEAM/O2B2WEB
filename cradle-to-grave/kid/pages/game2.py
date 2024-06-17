import random

import streamlit as st

st.set_page_config(
    page_title="노세老世",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Initialize session state variables
if 'player_hand' not in st.session_state:
    st.session_state.player_hand = []
if 'computer_hand' not in st.session_state:
    st.session_state.computer_hand = []
if 'deck' not in st.session_state:
    st.session_state.deck = []
if 'field' not in st.session_state:
    st.session_state.field = []
if 'player_score' not in st.session_state:
    st.session_state.player_score = 0
if 'computer_score' not in st.session_state:
    st.session_state.computer_score = 0

# Hwatu card list
cards = [
    "1월 홍단", "1월 초단", "1월 말단", "1월 끗",
    "2월 홍단", "2월 초단", "2월 말단", "2월 끗",
    "3월 홍단", "3월 초단", "3월 말단", "3월 끗",
    "4월 흑단", "4월 초단", "4월 말단", "4월 끗",
    "5월 흑단", "5월 초단", "5월 말단", "5월 끗",
    "6월 청단", "6월 초단", "6월 말단", "6월 끗",
    "7월 청단", "7월 초단", "7월 말단", "7월 끗",
    "8월 청단", "8월 초단", "8월 말단", "8월 끗",
    "9월 초단", "9월 말단", "9월 끗", "9월 특수",
    "10월 청단", "10월 초단", "10월 말단", "10월 끗",
    "11월 청단", "11월 초단", "11월 말단", "11월 끗",
    "12월 청단", "12월 말단", "12월 끗",
    "12월 특수"
]

# Map card names to image file names
card_images = {card: f"images/{card}.png" for card in cards}

# Function to reset the game
def reset_game():
    st.session_state.deck = cards.copy()
    random.shuffle(st.session_state.deck)
    st.session_state.field = [st.session_state.deck.pop() for _ in range(8)]
    st.session_state.player_hand = [st.session_state.deck.pop() for _ in range(10)]
    st.session_state.computer_hand = [st.session_state.deck.pop() for _ in range(10)]
    st.session_state.player_score = 0
    st.session_state.computer_score = 0



# Function to handle player's turn
def player_turn(card):
    st.session_state.player_hand.remove(card)
    st.session_state.field.append(card)
    check_for_matches(card, 'player')
    computer_turn()

# Function to handle computer's turn
def computer_turn():
    if st.session_state.computer_hand:
        card = random.choice(st.session_state.computer_hand)
        st.session_state.computer_hand.remove(card)
        st.session_state.field.append(card)
        check_for_matches(card, 'computer')

# Function to check for matches and update scores
def check_for_matches(card, player):
    month = card.split(' ')[0]
    matches = [c for c in st.session_state.field if c.split(' ')[0] == month]
    if len(matches) >= 2:
        if player == 'player':
            st.session_state.player_score += len(matches)
        else:
            st.session_state.computer_score += len(matches)
        for match in matches:
            st.session_state.field.remove(match)

st.subheader("노세老世 | 두뇌개발", divider='orange')

col1, col2 = st.columns([7, 1])
with col1:
    st.header("맞고 :sunrise_over_mountains:")

with col2:
    # Ensure the game is started/reset at the beginning
    if st.button("게임 시작"):
        reset_game()
st.markdown(" ")
col1, col2 = st.columns(2)
with col1:
    with st.container():
        st.subheader("필드")
        field_images = [card_images[card] for card in st.session_state.field]
        st.image(field_images, width=100, caption=st.session_state.field)
with col2:
    with st.container():
        st.subheader("플레이어")
        player_images = [card_images[card] for card in st.session_state.player_hand]
        st.image(player_images, width=100, caption=st.session_state.player_hand)

col1, col2 = st.columns([4, 1])
with col1:
    if st.session_state.player_hand:
        cols = st.columns(len(st.session_state.player_hand))
        for idx, card in enumerate(st.session_state.player_hand):
            with cols[idx]:
                if st.button(f"{card}", key=card):
                    player_turn(card)
                    break  # Ensure only one card is played per click
    else:
        st.write("No cards in hand.")
with col2:
    with st.container():
        st.subheader("점수")
        st.write(f"🧑‍🎓: {st.session_state.player_score}")
        st.write(f"💻: {st.session_state.computer_score}")
        if st.session_state.player_score >= 10:
            st.success("플레이어 승리!")
        elif st.session_state.computer_score >= 10:
            st.error("컴퓨터 승리!")
st.markdown("")
st.markdown("")
st.markdown("")
st.markdown("")
st.markdown("")
st.markdown("---")
st.markdown('''
### 규칙 
- **카드 구성**: 화투 카드 48장을 사용합니다.
- **플레이어**: 2명의 플레이어 (플레이어와 컴퓨터).
- **카드 배분**: 각 플레이어는 10장의 카드를 받고, 필드에는 8장의 카드가 놓입니다. 나머지 카드는 덱으로 사용됩니다.

### 게임 진행

- **게임 시작**: "게임 시작" 버튼을 눌러 게임을 시작합니다.
- **플레이어 턴**: 플레이어는 자신의 손패에서 카드를 선택하여 필드에 냅니다. 만약 필드에 같은 달의 카드가 있으면 해당 카드를 가져와 매칭합니다. 그렇지 않으면 필드에 카드를 놓습니다.
- **컴퓨터 턴**: 플레이어가 카드를 낸 후, 컴퓨터도 랜덤으로 카드를 선택하여 필드에 내고, 같은 방식으로 매칭을 시도합니다.
- **점수 계산**: 같은 달의 카드가 필드에 2장 이상 있을 때, 매칭된 카드 수만큼 점수를 얻습니다. 플레이어와 컴퓨터는 각각 매칭된 카드의 수에 따라 점수를 획득합니다.

### 점수와 승리

- **점수 획득**: 매칭된 카드로 점수를 얻습니다. 매칭된 카드의 수만큼 점수를 추가합니다.
- **승리 조건**: 플레이어 또는 컴퓨터가 10점 이상을 먼저 달성하면 승리합니다.
  - 플레이어가 10점 이상일 경우 "플레이어 승리!" 메시지가 표시됩니다.
  - 컴퓨터가 10점 이상일 경우 "컴퓨터 승리!" 메시지가 표시됩니다.

이 게임은 각 플레이어가 번갈아가며 카드를 내고, 필드에서 매칭되는 카드를 통해 점수를 획득하는 방식으로 진행됩니다. 10점 이상을 먼저 달성하는 플레이어가 승리합니다.
''')
