import streamlit as st
import random
import time

# 1. 페이지 설정
st.set_page_config(page_title="JAEGOOK LIVE STUDIO", page_icon="🎰", layout="wide")

# 2. 상태 초기화
if 'balance' not in st.session_state: st.session_state.balance = 100000
if 'history' not in st.session_state: st.session_state.history = []
if 'game_started' not in st.session_state: st.session_state.game_started = False
if 'bet_placed' not in st.session_state: st.session_state.bet_placed = None
if 'bet_amount' not in st.session_state: st.session_state.bet_amount = 0

# 3. 사진 UI 완벽 재현 CSS
st.markdown("""
    <style>
    .main { background-color: #050505; }
    /* 상단 레드 테이블 & 딜러 */
    .table-top {
        background: radial-gradient(circle, #b22222 0%, #3d0000 100%);
        height: 380px; border-radius: 0 0 50% 50% / 0 0 15% 15%;
        border-bottom: 8px solid #5d4037; position: relative; text-align: center;
        box-shadow: 0 15px 40px rgba(0,0,0,0.8);
    }
    .dealer-img { width: 180px; margin-top: 15px; border-radius: 50%; border: 3px solid #f1c40f; }
    
    /* 카드 애니메이션 (던지는 효과) */
    .card-fly {
        display: inline-block; font-size: 70px; margin: 10px;
        animation: throw 0.6s ease-out forwards; opacity: 0;
    }
    @keyframes throw {
        0% { transform: translateY(-200px) scale(0.5); opacity: 0; }
        100% { transform: translateY(0) scale(1); opacity: 1; }
    }

    /* 하단 베팅 존 (사진 레이아웃) */
    .betting-area {
        display: flex; justify-content: center; gap: 15px; margin-top: 40px;
    }
    .stButton>button {
        height: 120px !important; border-radius: 15px !important; font-size: 22px !important;
        font-weight: bold !important; border: 2px solid #444 !important;
    }
    .p-btn { background-color: rgba(231, 76, 60, 0.1) !important; color: #e74c3c !important; }
    .b-btn { background-color: rgba(52, 152, 219, 0.1) !important; color: #3498db !important; }
    .t-btn { background-color: rgba(46, 204, 113, 0.1) !important; color: #2ecc71 !important; }

    /* 우측 하단 기록지 */
    .log-panel {
        position: fixed; bottom: 20px; right: 20px;
        background: rgba(0,0,0,0.8); padding: 12px; border-radius: 8px;
        border: 1px solid #333; display: grid; grid-template-columns: repeat(6, 22px); gap: 5px;
    }
    .log-dot { width: 20px; height: 20px; border-radius: 50%; font-size: 11px; text-align: center; line-height: 20px; color: white; font-weight: bold; }
    
    .timer-text { font-size: 45px; color: #f1c40f; font-weight: bold; text-shadow: 0 0 15px #f1c40f; }
    </style>
    """, unsafe_allow_html=True)

# 4. 긴장감 넘치는 BGM
st.markdown('<iframe src="https://www.youtube.com/embed/fZZS8GZStUw?autoplay=1&loop=1&playlist=fZZS8GZStUw" width="0" height="0" frameborder="0" allow="autoplay"></iframe>', unsafe_allow_html=True)

# --- [인트로] ---
if not st.session_state.game_started:
    st.video("game/intro.mp4")
    if st.button("🧧 STUDIO ENTER", use_container_width=True):
        st.session_state.game_started = True
        st.rerun()

# --- [라이브 스튜디오] ---
else:
    # 1. 상단 스튜디오 구역
    st.markdown("<div class='table-top'>", unsafe_allow_html=True)
    try:
        st.image("game/dealer.jpg", width=180) # 딜러 중앙 배치
    except:
        st.write("👤 [WAITING FOR DEALER]")
    
    timer_placeholder = st.empty()
    card_placeholder = st.empty()
    st.markdown("</div>", unsafe_allow_html=True)

    # 2. 잔액 정보
    st.markdown(f"<h2 style='text-align:center; color:white; margin-top:20px;'>💰 자산: {st.session_state.balance:,}원</h2>", unsafe_allow_html=True)

    # 3. 게임 엔진 (10초 카운트다운 루프)
    if st.session_state.bet_placed is None:
        # 베팅 선택 UI (슬라이더로 금액 조절)
        st.write("---")
        bet_amt = st.select_slider("베팅 칩 선택", options=[1000, 5000, 10000, 50000, 100000], value=5000)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("👤 PLAYER (2.0x)", use_container_width=True, key="p"):
                st.session_state.bet_placed = "P"; st.session_state.bet_amount = bet_amt; st.rerun()
        with col2:
            if st.button("👔 TIE (9.0x)", use_container_width=True, key="t"):
                st.session_state.bet_placed = "T"; st.session_state.bet_amount = bet_amt; st.rerun()
        with col3:
            if st.button("🏦 BANKER (1.95x)", use_container_width=True, key="b", type="primary"):
                st.session_state.bet_placed = "B"; st.session_state.bet_amount = bet_amt; st.rerun()

        # 대기 시간 카운트다운 (아무것도 안 누를 때)
        for i in range(10, -1, -1):
            timer_placeholder.markdown(f"<p class='timer-text' style='text-align:center;'>PLACE YOUR BETS: {i}s</p>", unsafe_allow_html=True)
            time.sleep(1)
        st.rerun()

    else:
        # 베팅 완료 후 딜링 시작
        st.session_state.balance -= st.session_state.bet_amount
        timer_placeholder.markdown("<p class='timer-text' style='text-align:center; color:#e74c3c;'>NO MORE BETS</p>", unsafe_allow_html=True)
        time.sleep(1.5)

        # 카드 셔플 및 결과 계산
        deck = [f"{s}{r}" for s in ['♠️','♥️','♣️','♦️'] for r in ['A','2','3','4','5','6','7','8','9','10','J','Q','K']]
        random.shuffle(deck)
        p_h, b_h = [deck.pop(), deck.pop()], [deck.pop(), deck.pop()]
        
        def score(h):
            s = 0
            for c in h:
                v = c[2:]
                if v in ['J','Q','K','10']: s += 0
                elif v == 'A': s += 1
                else: s += int(v)
            return s % 10

        ps, bs = score(p_h), score(b_h)

        # 딜러가 카드를 던지는 연출 (애니메이션)
        timer_placeholder.empty()
        card_placeholder.markdown(f"""
            <div style='display:flex; justify-content:center; gap:80px; margin-top:200px;'>
                <div class='card-fly' style='color:#e74c3c;'>PLAYER: {ps}<br>{' '.join(p_h)}</div>
                <div class='card-fly' style='color:#3498db;'>BANKER: {bs}<br>{' '.join(b_h)}</div>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(1.5)

        # 승패 판정
        res = "T" if ps == bs else ("P" if ps > bs else "B")
        st.session_state.history.append(res)
        
        if (st.session_state.bet_placed == "P" and res == "P"): st.session_state.balance += st.session_state.bet_amount * 2; st.balloons()
        elif (st.session_state.bet_placed == "B" and res == "B"): st.session_state.balance += int(st.session_state.bet_amount * 1.95); st.balloons()
        elif (st.session_state.bet_placed == "T" and res == "T"): st.session_state.balance += st.session_state.bet_amount * 9; st.balloons()
        
        time.sleep(3)
        st.session_state.bet_placed = None
        st.rerun()

    # 4. 우측 하단 기록지
    log_html = "<div class='log-panel'>"
    for r in st.session_state.history[-30:]:
        color = "#e74c3c" if r == "P" else ("#3498db" if r == "B" else "#2ecc71")
        log_html += f"<div class='log-dot' style='background:{color}'>{r}</div>"
    log_html += "</div>"
    st.markdown(log_html, unsafe_allow_html=True)