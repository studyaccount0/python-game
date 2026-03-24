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
        # 영상만 깔끔하게 출력
        st.video("./game/intro.mp4")
    except:
        st.error("intro.mp4 파일을 확인해주세요.")
    
    st.write("")
    if st.button("🚀 게임 실행", use_container_width=True):
        st.session_state.game_started = True
        st.rerun()

# --- [바카라 게임 화면] ---
else:
    st.markdown("""
        <style>
        .main { background-color: #064e3b; color: white; }
        .stButton>button { width: 100%; font-weight: bold; border-radius: 10px; }
        .balance-box { font-size: 24px; background-color: #f1c40f; color: black; padding: 10px; border-radius: 10px; text-align: center; font-weight: bold; margin-bottom: 20px; }
        .card-val { font-size: 35px; font-weight: bold; color: #f1c40f; }
        </style>
        """, unsafe_allow_html=True)

    # 상단 자산 표시
    st.markdown(f"<div class='balance-box'>💰 현재 잔액: {st.session_state.balance:,}원</div>", unsafe_allow_html=True)
    st.title("🎰 HIGH LIMIT BACCARAT")

    # 베팅 설정 구역 (들여쓰기 완벽 수정)
    st.write("---")
    col_bet1, col_bet2 = st.columns([2, 1])
    with col_bet1:
        bet_target = st.radio("어디에 베팅하시겠습니까?", ["플레이어(2배)", "뱅커(1.95배)", "타이(9배)"], horizontal=True)
    with col_bet2:
        # 이 부분이 아까 에러가 났던 곳입니다. 들여쓰기와 괄호를 맞췄습니다.
        bet_amount = st.number_input("베팅 금액", min_value=1000, max_value=st.session_state.balance, step=1000, value=1000)

    # 카드 점수 계산 함수
    def get_score(cards):
        score = 0
        for c in cards:
            val = c.split()[1]
            if val in ['J', 'Q', 'K', '10']: score += 0
            elif val == 'A': score += 1
            else: score += int(val)
        return score % 10

    # 게임 실행 버튼
    if st.button("🃏 DEAL (카드 뽑기)", type="primary"):
        if st.session_state.balance < bet_amount:
            st.error("잔액이 부족합니다!")
        else:
            # 베팅금 차감
            st.session_state.balance -= bet_amount
            
            # 카드 덱 생성 및 셔플
            suits = ['♠️', '♥️', '♣️', '♦️']
            ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
            deck = [f"{s} {r}" for s in suits for r in ranks]
            random.shuffle(deck)

            p_cards = [deck.pop(), deck.pop()]
            b_cards = [deck.pop(), deck.pop()]
            p_score = get_score(p_cards)
            b_score = get_score(b_cards)

            with st.spinner("딜링 중..."):
                time.sleep(1)

            c1, c2 = st.columns(2)
            with c1:
                st.subheader("👤 PLAYER")
                st.write(f"### {' '.join(p_cards)}")
                st.markdown(f"<p class='card-val'>{p_score}</p>", unsafe_allow_html=True)
            with c2:
                st.subheader("🏦 BANKER")
                st.write(f"### {' '.join(b_cards)}")
                st.markdown(f"<p class='card-val'>{b_score}</p>", unsafe_allow_html=True)

            # 결과 판정
            result = ""
            if p_score > b_score: result = "플레이어(2배)"
            elif b_score > p_score: result = "뱅커(1.95배)"
            else: result = "타이(9배)"

            st.write("---")
            if bet_target == result:
                if result == "플레이어(2배)": win_money = bet_amount * 2
                elif result == "뱅커(1.95배)": win_money = int(bet_amount * 1.95)
                else: win_money = bet_amount * 9
                
                st.session_state.balance += win_money
                st.balloons()
                st.success(f"축하합니다! 베팅 성공! {win_money:,}원을 획득하셨습니다.")
            else:
                st.error(f"아쉽습니다. 결과는 {result.split('(')[0]}입니다.")

    # 사이드바 메뉴
    st.sidebar.write(f"### 내 자산: {st.session_state.balance:,}원")
    if st.sidebar.button("🏠 처음으로 돌아가기"):
        st.session_state.game_started = False
        st.rerun()
    if st.sidebar.button("💸 자금 충전 (10만원)"):
        st.session_state.balance = 100000
        st.rerun()