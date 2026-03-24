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

# 3. 사진 UI 완벽 재현 CSS (테이블 위에 딜러 고정)
st.markdown("""
    <style>
    .main { background-color: #050505; }
    
    /* 실제 사진처럼 빨간 테이블 중앙에 딜러 배치 */
    .studio-container {
        background: radial-gradient(circle, #b22222 0%, #3d0000 100%);
        height: 500px; border-radius: 0 0 50% 50% / 0 0 15% 15%;
        border-bottom: 10px solid #5d4037; position: relative;
        display: flex; flex-direction: column; align-items: center; justify-content: flex-start;
        box-shadow: 0 20px 50px rgba(0,0,0,0.8); overflow: hidden;
    }
    .dealer-img {
        width: 200px; margin-top: 30px; border-radius: 20px;
        border: 4px solid #f1c40f; z-index: 10;
    }
    
    /* 카드 한 장씩 던지는 애니메이션 */
    .card-slot {
        font-size: 80px; display: inline-block; margin: 15px;
        animation: card-entry 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
    }
    @keyframes card-entry {
        0% { transform: translateY(-300px) rotate(180deg) scale(0); opacity: 0; }
        100% { transform: translateY(0) rotate(0deg) scale(1); opacity: 1; }
    }

    /* 하단 베팅 구역 디자인 */
    .betting-board { display: flex; justify-content: center; gap: 20px; margin-top: 50px; }
    .stButton>button {
        height: 100px !important; border-radius: 12px !important;
        font-size: 24px !important; font-weight: bold !important;
    }
    
    /* 우측 하단 스코어 보드 */
    .roadmap {
        position: fixed; bottom: 30px; right: 30px;
        background: rgba(0,0,0,0.85); padding: 15px; border-radius: 10px;
        border: 2px solid #444; display: grid; grid-template-columns: repeat(6, 25px); gap: 6px;
    }
    .dot { width: 22px; height: 22px; border-radius: 50%; font-size: 12px; text-align: center; line-height: 22px; color: white; font-weight: bold; }
    
    .timer { font-size: 50px; color: #f1c40f; font-weight: bold; text-shadow: 0 0 20px #f1c40f; margin-top: 100px; }
    </style>
    """, unsafe_allow_html=True)

# 4. 배경음악 (긴장감 루프)
st.markdown('<iframe src="https://www.youtube.com/embed/fZZS8GZStUw?autoplay=1&loop=1&playlist=fZZS8GZStUw" width="0" height="0" frameborder="0" allow="autoplay"></iframe>', unsafe_allow_html=True)

# --- [인트로] ---
if not st.session_state.game_started:
    st.video("game/intro.mp4")
    if st.button("🧧 STUDIO LOGIN (입장)", use_container_width=True):
        st.session_state.game_started = True
        st.rerun()

# --- [메인 스튜디오 화면] ---
else:
    # 1. 상단: 레드 테이블 + 재국님(딜러) 사진 중앙 배치
    st.markdown("<div class='studio-container'>", unsafe_allow_html=True)
    try:
        # 사진에서 보신 것처럼 딜러가 테이블 중앙 상단에 위치하도록 설정
        st.image("game/dealer.jpg", width=200) 
    except:
        st.write("👤 [WAITING FOR DEALER...]")
    
    timer_placeholder = st.empty()
    card_placeholder = st.empty()
    st.markdown("</div>", unsafe_allow_html=True)

    # 2. 잔액 표시
    st.markdown(f"<h1 style='text-align:center; color:white;'>💰 BALANCE: {st.session_state.balance:,}원</h1>", unsafe_allow_html=True)

    # 3. 게임 엔진 (베팅 15초)
    if st.session_state.bet_placed is None:
        st.write("---")
        bet_amt = st.select_slider("BETTING CHIP", options=[1000, 5000, 10000, 50000, 100000, 500000], value=10000)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("👤 PLAYER\n(2.0x)", use_container_width=True):
                st.session_state.bet_placed = "P"; st.session_state.bet_amount = bet_amt; st.rerun()
        with c2:
            if st.button("👔 TIE\n(9.0x)", use_container_width=True):
                st.session_state.bet_placed = "T"; st.session_state.bet_amount = bet_amt; st.rerun()
        with c3:
            if st.button("🏦 BANKER\n(1.95x)", use_container_width=True, type="primary"):
                st.session_state.bet_placed = "B"; st.session_state.bet_amount = bet_amt; st.rerun()

        # 베팅 시간 15초 카운트다운
        for i in range(15, -1, -1):
            timer_placeholder.markdown(f"<div class='timer' style='text-align:center;'>PLACE YOUR BETS: {i}s</div>", unsafe_allow_html=True)
            time.sleep(1)
        st.rerun()

    else:
        # 베팅 완료 후 카드 오픈 (15초간 한 장씩 천천히)
        st.session_state.balance -= st.session_state.bet_amount
        timer_placeholder.markdown("<div class='timer' style='text-align:center; color:#e74c3c;'>NO MORE BETS</div>", unsafe_allow_html=True)
        time.sleep(2)

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

        # 카드 한 장씩 공개 (총 15초 소요 연출)
        timer_placeholder.empty()
        display_cards = {"P": [], "B": []}
        
        for i in range(2):
            display_cards["P"].append(p_h[i])
            card_placeholder.markdown(f"""
                <div style='display:flex; justify-content:center; gap:100px; margin-top:150px;'>
                    <div class='card-slot' style='color:#e74c3c;'>PLAYER<br>{' '.join(display_cards["P"])}</div>
                    <div class='card-slot' style='color:#3498db;'>BANKER<br>{' '.join(display_cards["B"])}</div>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(3.5) # 한 장당 약 3.5초 (총 14~15초)
            
            display_cards["B"].append(b_h[i])
            card_placeholder.markdown(f"""
                <div style='display:flex; justify-content:center; gap:100px; margin-top:150px;'>
                    <div class='card-slot' style='color:#e74c3c;'>PLAYER<br>{' '.join(display_cards["P"])}</div>
                    <div class='card-slot' style='color:#3498db;'>BANKER<br>{' '.join(display_cards["B"])}</div>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(3.5)

        # 최종 점수 표시
        card_placeholder.markdown(f"""
            <div style='display:flex; justify-content:center; gap:100px; margin-top:150px;'>
                <div class='card-slot' style='color:#e74c3c;'>PLAYER: {ps}<br>{' '.join(p_h)}</div>
                <div class='card-slot' style='color:#3498db;'>BANKER: {bs}<br>{' '.join(b_h)}</div>
            </div>
        """, unsafe_allow_html=True)

        res = "T" if ps == bs else ("P" if ps > bs else "B")
        st.session_state.history.append(res)
        
        if (st.session_state.bet_placed == "P" and res == "P"): st.session_state.balance += st.session_state.bet_amount * 2; st.balloons()
        elif (st.session_state.bet_placed == "B" and res == "B"): st.session_state.balance += int(st.session_state.bet_amount * 1.95); st.balloons()
        elif (st.session_state.bet_placed == "T" and res == "T"): st.session_state.balance += st.session_state.bet_amount * 9; st.balloons()
        
        time.sleep(4)
        st.session_state.bet_placed = None
        st.rerun()

    # 4. 우측 하단 기록지 (로그)
    log_html = "<div class='roadmap'>"
    for r in st.session_state.history[-36:]:
        color = "#e74c3c" if r == "P" else ("#3498db" if r == "B" else "#2ecc71")
        log_html += f"<div class='dot' style='background:{color}'>{r}</div>"
    log_html += "</div>"
    st.markdown(log_html, unsafe_allow_html=True)