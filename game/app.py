import streamlit as st
import random
import time

# 1. 페이지 설정
st.set_page_config(page_title="JAEGOOK LIVE CASINO", page_icon="🧧", layout="wide")

# 2. 상태 초기화
if 'balance' not in st.session_state: st.session_state.balance = 100000
if 'history' not in st.session_state: st.session_state.history = []
if 'game_started' not in st.session_state: st.session_state.game_started = False
if 'bet_placed' not in st.session_state: st.session_state.bet_placed = None
if 'current_bet' not in st.session_state: st.session_state.current_bet = 1000

# 3. 사진과 똑같은 인터페이스를 위한 CSS (테이블 & 버튼 배치)
st.markdown("""
    <style>
    .main { background-color: #0a0a0a; }
    /* 상단 빨간 테이블 구역 */
    .casino-table {
        background: radial-gradient(circle, #b22222 0%, #4b0000 100%);
        height: 400px; border-radius: 50% / 20%;
        border: 10px solid #3e2723;
        margin: 0 auto; position: relative; text-align: center;
        box-shadow: 0 20px 50px rgba(0,0,0,0.9);
    }
    .dealer-container {
        position: absolute; top: 10%; left: 50%; transform: translateX(-50%);
        z-index: 10;
    }
    .dealer-img {
        width: 180px; border-radius: 50%; border: 4px solid #f1c40f;
        box-shadow: 0 0 20px rgba(241,196,15,0.5);
    }
    
    /* 카드 구역 */
    .card-area { position: absolute; bottom: 15%; width: 100%; display: flex; justify-content: center; gap: 50px; }
    .card-val { font-size: 50px; color: white; text-shadow: 2px 2px 5px black; }

    /* 하단 베팅 구역 (사진의 베팅존 재현) */
    .betting-floor {
        display: flex; justify-content: center; gap: 10px; margin-top: 30px;
    }
    .bet-box {
        background: rgba(255, 255, 255, 0.05); border: 2px solid #555;
        border-radius: 10px; padding: 20px; text-align: center; width: 200px;
        transition: 0.3s;
    }
    .bet-box:hover { border-color: #f1c40f; background: rgba(241, 196, 15, 0.1); }
    
    /* 타이머 및 자산 */
    .info-bar { text-align: center; margin-top: 20px; font-size: 24px; color: #f1c40f; }
    
    /* 우측 하단 기록지 */
    .roadmap-panel {
        position: fixed; bottom: 20px; right: 20px;
        background: rgba(0,0,0,0.85); padding: 10px; border-radius: 5px;
        border: 1px solid #444; display: grid; grid-template-columns: repeat(6, 20px); gap: 4px;
    }
    .dot { width: 18px; height: 18px; border-radius: 50%; font-size: 11px; font-weight: bold; text-align: center; line-height: 18px; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 배경음악 (자동재생)
st.markdown('<iframe src="https://www.youtube.com/embed/fZZS8GZStUw?autoplay=1&loop=1&playlist=fZZS8GZStUw" width="0" height="0" frameborder="0" allow="autoplay"></iframe>', unsafe_allow_html=True)

# --- [인트로] ---
if not st.session_state.game_started:
    st.video("game/intro.mp4")
    if st.button("🔥 라이브 카지노 접속", use_container_width=True):
        st.session_state.game_started = True
        st.rerun()

# --- [라이브 카지노 메인화면] ---
else:
    # 1. 상단: 빨간 테이블 + 중앙 딜러
    st.markdown("<div class='casino-table'>", unsafe_allow_html=True)
    st.markdown("<div class='dealer-container'>", unsafe_allow_html=True)
    try:
        st.image("game/dealer.jpg", width=180) # 딜러 사진
    except:
        st.write("👤 [딜러 대기중]")
    st.markdown("</div>", unsafe_allow_html=True)

    # 2. 중앙: 베팅 시간 카운트다운
    timer_area = st.empty()
    
    # 3. 카드 결과 노출 영역
    card_area = st.empty()
    st.markdown("</div>", unsafe_allow_html=True)

    # 4. 정보 바
    st.markdown(f"<div class='info-bar'>💰 MY BALANCE: {st.session_state.balance:,}원</div>", unsafe_allow_html=True)

    # 5. 하단: 사진과 똑같은 베팅존
    st.write("---")
    st.session_state.current_bet = st.select_slider("베팅 칩 선택", options=[1000, 5000, 10000, 50000, 100000], value=1000)

    col1, col2, col3 = st.columns(3)
    
    def run_deal(bet_target):
        if st.session_state.balance < st.session_state.current_bet:
            st.error("잔액이 부족합니다!")
            return

        st.session_state.balance -= st.session_state.current_bet
        
        # 딜링 연출
        for i in range(5, -1, -1):
            timer_area.markdown(f"<h2 style='text-align:center; color:red; margin-top:250px;'>NO MORE BETS: {i}s</h2>", unsafe_allow_html=True)
            time.sleep(0.5)
        
        # 카드 계산
        deck = [f"{s}{r}" for s in ['♠️','♥️','♣️','♦️'] for r in ['A','2','3','4','5','6','7','8','9','10','J','Q','K']]
        random.shuffle(deck)
        p_hand, b_hand = [deck.pop(), deck.pop()], [deck.pop(), deck.pop()]
        
        def get_s(h):
            s = 0
            for c in h:
                v = c[2:]
                if v in ['J','Q','K','10']: s += 0
                elif v == 'A': s += 1
                else: s += int(v)
            return s % 10

        ps, bs = get_s(p_hand), get_s(b_hand)
        
        # 카드 오픈 연출
        timer_area.empty()
        card_area.markdown(f"""
            <div class='card-area'>
                <div class='card-val'><span style='color:#e74c3c'>P</span> {ps} [ {' '.join(p_hand)} ]</div>
                <div class='card-val'><span style='color:#3498db'>B</span> {bs} [ {' '.join(b_hand)} ]</div>
            </div>
        """, unsafe_allow_html=True)

        res = "T" if ps == bs else ("P" if ps > bs else "B")
        st.session_state.history.append(res)

        if (bet_target == "P" and res == "P"): st.session_state.balance += st.session_state.current_bet * 2; st.balloons()
        elif (bet_target == "B" and res == "B"): st.session_state.balance += int(st.session_state.current_bet * 1.95); st.balloons()
        elif (bet_target == "T" and res == "T"): st.session_state.balance += st.session_state.current_bet * 9; st.balloons()
        
        time.sleep(3)
        st.rerun()

    with col1:
        if st.button("👤 PLAYER\n(2.0x)", use_container_width=True): run_deal("P")
    with col2:
        if st.button("👔 TIE\n(9.0x)", use_container_width=True): run_deal("T")
    with col3:
        if st.button("🏦 BANKER\n(1.95x)", use_container_width=True, type="primary"): run_deal("B")

    # 6. 우측 하단 기록지 (사진 UI)
    road_html = "<div class='roadmap-panel'>"
    for r in st.session_state.history[-30:]:
        color = "#e74c3c" if r == "P" else ("#3498db" if r == "B" else "#2ecc71")
        road_html += f"<div class='dot' style='background:{color}'>{r}</div>"
    road_html += "</div>"
    st.markdown(road_html, unsafe_allow_html=True)