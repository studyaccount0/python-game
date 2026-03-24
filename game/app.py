import streamlit as st
import random
import time

# 1. 초기 세팅
st.set_page_config(page_title="재국 vs AI 원카드", page_icon="🃏")

# 디자인 (초록색 테이블)
st.markdown("""
    <style>
    .main { background-color: #1a472a; color: white; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #f1c40f; color: black; }
    .card-box { padding: 10px; border: 2px solid white; border-radius: 10px; text-align: center; font-size: 25px; background-color: rgba(255,255,255,0.1); }
    </style>
    """, unsafe_allow_html=True)

# 2. 게임 데이터 초기화 (세션 상태)
if 'deck' not in st.session_state:
    suits = ['♠️', '♥️', '♣️', '♦️']
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    st.session_state.deck = [f"{s} {r}" for s in suits for r in ranks]
    random.shuffle(st.session_state.deck)
    
    # 처음 7장씩 나눠주기
    st.session_state.player_hand = [st.session_state.deck.pop() for _ in range(7)]
    st.session_state.ai_hand = [st.session_state.deck.pop() for _ in range(7)]
    # 바닥에 첫 카드 깔기
    st.session_state.top_card = st.session_state.deck.pop()
    st.session_state.turn = "Player"

# 3. 게임 로직 함수
def can_play(card, top_card):
    # 문양이나 숫자가 같으면 낼 수 있음
    s1, r1 = card.split()
    s2, r2 = top_card.split()
    return s1 == s2 or r1 == r2

def ai_play():
    time.sleep(1) # AI가 고민하는 척
    playable_cards = [c for c in st.session_state.ai_hand if can_play(c, st.session_state.top_card)]
    
    if playable_cards:
        chosen = random.choice(playable_cards)
        st.session_state.ai_hand.remove(chosen)
        st.session_state.top_card = chosen
        st.toast(f"AI가 {chosen}을 냈습니다!")
    else:
        st.session_state.ai_hand.append(st.session_state.deck.pop())
        st.toast("AI가 카드를 한 장 뽑았습니다.")
    st.session_state.turn = "Player"

# 4. 화면 구성
st.title("🃏 재국 vs 똑똑한 AI 원카드")
st.write(f"### 바닥 카드: **{st.session_state.top_card}**")
st.write(f"AI 남은 카드: {len(st.session_state.ai_hand)}장")

st.write("---")
st.subheader("내 손패 (클릭해서 카드 내기)")

# 내 카드 나열하기
cols = st.columns(len(st.session_state.player_hand))
for i, card in enumerate(st.session_state.player_hand):
    with cols[i]:
        if st.button(card, key=f"card_{i}"):
            if st.session_state.turn == "Player":
                if can_play(card, st.session_state.top_card):
                    st.session_state.player_hand.remove(card)
                    st.session_state.top_card = card
                    st.session_state.turn = "AI"
                    st.rerun()
                else:
                    st.error("낼 수 없는 카드입니다!")

# 카드 뽑기 버튼
if st.button("🎴 낼 게 없어서 한 장 뽑기"):
    if st.session_state.turn == "Player":
        st.session_state.player_hand.append(st.session_state.deck.pop())
        st.session_state.turn = "AI"
        st.rerun()

# 5. 승리 판정 및 AI 차례 실행
if len(st.session_state.player_hand) == 0:
    st.balloons()
    st.success("🎉 축하합니다! 당신이 이겼습니다!")
    if st.button("게임 다시 시작"): st.session_state.clear(); st.rerun()
elif len(st.session_state.ai_hand) == 0:
    st.error("💀 AI가 승리했습니다... 다시 도전해보세요!")
    if st.button("게임 다시 시작"): st.session_state.clear(); st.rerun()

if st.session_state.turn == "AI":
    with st.spinner("AI가 생각 중..."):
        ai_play()
        st.rerun()