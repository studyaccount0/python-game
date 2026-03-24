import streamlit as st
import random
import time

# 1. 페이지 설정
st.set_page_config(page_title="재국 바카라: 카지노", page_icon="💰")

# 2. 게임 상태 및 자산 초기화
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'balance' not in st.session_state:
    st.session_state.balance = 100000  # 초기 자금 10만원

# --- [인트로 화면] ---
if not st.session_state.game_started:
    try:
        st.video("intro.mp4")
    except:
        st.error("intro.mp4 파일이 없습니다.")
    
    st.write("")
    if st.button("🚀 카지노 입장하기 (자산: 100,000원)", use_container_width=True):
        st.session_state.game_started = True
        st.rerun()

# --- [바카라 게임 화면] ---
else:
    st.markdown("""
        <style>
        .main { background-color: #064e3b; color: white; }
        .stButton>button { width: 100%; font-weight: bold; border-radius: 10px; }
        .balance-box { font-size: 24px; background-color: #f1c40f; color: black; padding: 10px; border-radius: 10px; text-align: center; font-weight: bold; }
        .card-val { font-size: 35px; font-weight: bold; color: #f1c40f; }
        </style>
        """, unsafe_allow_html=True)

    # 상단 자산 표시
    st.markdown(f"<div class='balance-box'>현재 잔액: {st.session_state.balance:,}원</div>", unsafe_allow_html=True)
    st.title("🎰 HIGH LIMIT BACCARAT")

    # 베팅 설정 구역
    st.write("---")
    col_bet1, col_bet2 = st.columns([2, 1])
    with col_bet1:
        bet_target = st.radio("어디에 베팅하시겠습니까?", ["플레이어(2배)", "뱅커(1.95배)", "타이(9배)"], horizontal=True)
    with col_bet2:
        bet_amount = st.number_input("베팅 금액", min_value=1000, max_value=st.session_state.balance, step=1000, value=1000