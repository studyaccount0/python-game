import streamlit as st
import random
import time

# 1. 페이지 설정 (넓은 화면 모드)
st.set_page_config(page_title="재국 라이브 카지노", page_icon="🎰", layout="wide")

# 2. 게임 상태 초기화
if 'balance' not in st.session_state:
    st.session_state.balance = 100000
if 'history' not in st.session_state:
    st.session_state.history = []
if 'game_started' not in st.session_state:
    st.session_state.game_started = False

# 3. 사진과 똑같은 레이아웃을 위한 CSS
st.markdown("""
    <style>
    .main { background-color: #0d0d0d; }
    /* 중앙 딜러 테이블 */
    .casino-floor {
        background: radial-gradient(circle, #a52a2a 0%, #3d0000 100%);
        border-radius: 50% / 20%;
        padding: 50px;
        border: 8px solid #5d4037;
        text-align: center;
        position: relative;
        min-height: 400px;
        margin-bottom: 20px;
    }
    .dealer-box { position: absolute; top: -20px; left: 50%; transform: translateX(-50%); }
    .card-display { font-size: 70px; margin: 10px; animation: flip 0.5s ease-in-out; display: inline-block; }
    @keyframes flip { from { transform: rotateY(90deg); } to { transform: rotateY(0deg); } }
    
    /* 하단 베팅 구역 */
    .bet-zone { background: #1a1a1a; padding: 20px; border-radius: 15px; border-top: 3px solid #f1c40f; }
    .bet-btn { height: 100px !important; font-size: 20px !important; }
    
    /* 우측 하단 기록지(스코어보드) */
    .score-board {
        position: fixed; bottom: 20px; right: 20px;
        background: rgba(0,0,0,0.8); padding: 10px; border-radius: 10px;
        border: 1px solid #444; width: 250px; z-index: 100;
    }
    .dot { display: inline-block; width: 20px; height: 20px; border-radius: 50%; margin: 2px; text-align: center; font-size: 12px; color: white; line-height: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- [인트로: 영상] ---
if not st.session_state.game_started:
    st.video("game/intro.mp4")
    if st.button("🔥 카지노 입장 (GAME START)", use_container_width=True):
        st.session_state.game_started = True
        st.rerun()

# --- [메인: 라이브 카지노] ---
else:
    # 1. 상단 테이블 (딜러와 카드)
    st.markdown("<div class='casino-floor'>", unsafe_allow_html=True)
    col_d1, col_d2, col_d3 = st.columns([1, 2, 1])
    with col_d2:
        try:
            st.image("game/dealer.jpg", width=250) # 중앙에 앉아있는 딜러
        except:
            st.write("👤 [딜러 대기 중]")
    
    # 카드 출력 공간 (베팅 후 나타남)
    p_space, b_space = st.columns(2)
    st.markdown("</div>", unsafe_allow_html=True)

    # 2. 정보 바
    st.markdown(f"<h2 style='text-align:center;'>💰 잔액: {st.session_state.balance:,}원</h2>", unsafe_allow_html=True)

    # 3. 하단 베팅 존 (사진처럼 배수 표시 및 클릭 베팅)
    st.markdown("<div class='bet-zone'>", unsafe_allow_html=True)
    
    # 베팅 금액 설정
    bet_amt = st.select_slider("베팅 금액 선택", options=[1000, 5000, 10000, 50000, 100000], value=1000)
    
    col1, col2, col3 = st.columns(3)
    
    # 게임 로직 함수
    def play_game(target):
        if st.session_state.balance < bet_amt:
            st.error("잔액이 부족합니다!")
            return

        st.session_state.balance -= bet_amt
        suits = ['♠️', '♥️', '♣️', '♦️']
        ranks = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
        deck = [f"{s}{r}" for s in suits for r in ranks]
        random.shuffle(deck)

        p_cards = [deck.pop(), deck.pop()]
        b_cards = [deck.pop(), deck.pop()]
        
        # 단순 점수 계산 (바카라 룰)
        def get_s(cards):
            s = 0
            for c in cards:
                v = c[2:]
                if v in ['J','Q','K','10']: s += 0
                elif v == 'A': s += 1
                else: s += int(v)
            return s % 10

        ps, bs = get_s(p_cards), get_s(b_cards)
        
        # 카드 공개 애니메이션 연출
        with st.spinner("카드를 오픈합니다..."):
            time.sleep(1)
            with p_space:
                st.subheader(f"PLAYER: {ps}")
                st.markdown(f"<div class='card-display'>{' '.join(p_cards)}</div>", unsafe_allow_html=True)
            with b_space:
                st.subheader(f"BANKER: {bs}")
                st.markdown(f"<div class='card-display'>{' '.join(b_cards)}</div>", unsafe_allow_html=True)

        # 결과 판정
        res = "T" if ps == bs else ("P" if ps > bs else "B")
        st.session_state.history.append(res)
        
        if (target == "PLAYER" and res == "P"):
            st.session_state.balance += bet_amt * 2
            st.balloons()
        elif (target == "BANKER" and res == "B"):
            st.session_state.balance += int(bet_amt * 1.95)
            st.balloons()
        elif (target == "TIE" and res == "T"):
            st.session_state.balance += bet_amt * 9
            st.balloons()
        
        time.sleep(2)
        st.rerun()

    with col1:
        if st.button(f"👤 PLAYER\n(2.0x)", use_container_width=True, key="p_btn"):
            play_game("PLAYER")
    with col2:
        if st.button(f"👔 TIE\n(9.0x)", use_container_width=True, key="t_btn"):
            play_game("TIE")
    with col3:
        if st.button(f"🏦 BANKER\n(1.95x)", use_container_width=True, key="b_btn", type="primary"):
            play_game("BANKER")
    st.markdown("</div>", unsafe_allow_html=True)

    # 4. 우측 하단 기록지 (사진의 전 결과들)
    history_html = "<div class='score-board'><b>LOG</b><br>"
    for r in st.session_state.history[-15:]:
        color = "#e74c3c" if r == "P" else ("#3498db" if r == "B" else "#2ecc71")
        history_html += f"<span class='dot' style='background:{color}'>{r}</span>"
    history_html += "</div>"
    st.markdown(history_html, unsafe_allow_html=True)

    # 사이드바 충전
    st.sidebar.button("💰 10만 원 충전", on_click=lambda: st.session_state.update(balance=100000))