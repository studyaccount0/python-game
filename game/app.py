import streamlit as st
import random
import time
import os

# 1. 페이지 설정
st.set_page_config(page_title="JAEGOOK LIVE CASINO", page_icon="🧧", layout="wide")

# 2. 상태 초기화
if 'balance' not in st.session_state: st.session_state.balance = 100000
if 'history' not in st.session_state: st.session_state.history = []
if 'game_started' not in st.session_state: st.session_state.game_started = False
if 'bet_placed' not in st.session_state: st.session_state.bet_placed = None
if 'current_bet' not in st.session_state: st.session_state.current_bet = 0

# 3. 사진과 흡사한 라이브 UI 전용 CSS
st.markdown("""
    <style>
    .main { background-color: #050505; }
    /* 상단 테이블 & 딜러 */
    .live-studio {
        background: radial-gradient(circle, #8b0000 0%, #200000 100%);
        border-bottom: 5px solid #d4af37;
        height: 450px; position: relative; text-align: center;
        border-radius: 0 0 50% 50% / 0 0 20% 20%;
    }
    .dealer-img { width: 200px; margin-top: 20px; border-radius: 50%; border: 3px solid #d4af37; }
    
    /* 베팅 타이머 */
    .timer-text { font-size: 40px; color: #ff0000; font-weight: bold; text-shadow: 0 0 10px #ff0000; }
    
    /* 하단 베팅 구역 (사진 UI 재현) */
    .bet-container {
        position: fixed; bottom: 0; left: 0; right: 0;
        background: rgba(20, 20, 20, 0.95); padding: 20px;
        border-top: 2px solid #444; display: flex; justify-content: center; gap: 10px;
    }
    .bet-card {
        border: 2px solid #555; border-radius: 10px; padding: 15px; text-align: center;
        min-width: 150px; transition: 0.3s; cursor: pointer;
    }
    .bet-card:hover { border-color: #f1c40f; background: rgba(241, 196, 15, 0.1); }
    .bet-p { color: #e74c3c; font-weight: bold; }
    .bet-b { color: #3498db; font-weight: bold; }
    .bet-t { color: #2ecc71; font-weight: bold; }

    /* 우측 하단 기록지 */
    .roadmap {
        position: fixed; bottom: 120px; right: 20px;
        background: rgba(0,0,0,0.7); padding: 10px; border-radius: 5px;
        display: grid; grid-template-columns: repeat(6, 1fr); gap: 3px;
    }
    .road-dot { width: 18px; height: 18px; border-radius: 50%; font-size: 10px; text-align: center; line-height: 18px; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 4. 배경음악(BGM) 추가
# 긴장감 있는 루프 음악 (유튜브 라이브 카지노 느낌)
st.markdown("""
    <iframe src="https://www.youtube.com/embed/fZZS8GZStUw?autoplay=1&loop=1&playlist=fZZS8GZStUw" 
    width="0" height="0" frameborder="0" allow="autoplay"></iframe>
    """, unsafe_allow_html=True)

# --- [인트로 화면] ---
if not st.session_state.game_started:
    st.video("game/intro.mp4")
    if st.button("🧧 카지노 입장하기 (ENTER STUDIO)", use_container_width=True):
        st.session_state.game_started = True
        st.rerun()

# --- [메인 라이브 화면] ---
else:
    # 1. 라이브 스튜디오 (상단)
    st.markdown("<div class='live-studio'>", unsafe_allow_html=True)
    try:
        st.image("game/dealer.jpg", width=220)
    except:
        st.write("👤 [딜러 입장 중...]")
    
    # 베팅 타이머 표시
    timer_placeholder = st.empty()
    st.markdown("</div>", unsafe_allow_html=True)

    # 2. 게임 영역 (카드 오픈 시 사용)
    card_col1, card_col2 = st.columns(2)
    
    # 3. 우측 하단 기록지 (사진 UI)
    road_html = "<div class='roadmap'>"
    for r in st.session_state.history[-36:]:
        color = "#e74c3c" if r == "P" else ("#3498db" if r == "B" else "#2ecc71")
        road_html += f"<div class='road-dot' style='background:{color}'>{r}</div>"
    road_html += "</div>"
    st.markdown(road_html, unsafe_allow_html=True)

    # 4. 베팅 로직
    if st.session_state.bet_placed is None:
        # 10초 카운트다운 시작
        for i in range(10, -1, -1):
            timer_placeholder.markdown(f"<p class='timer-text' style='text-align:center;'>PLACE YOUR BETS: {i}s</p>", unsafe_allow_html=True)
            if i == 0:
                timer_placeholder.markdown("<p class='timer-text' style='text-align:center;'>NO MORE BETS</p>", unsafe_allow_html=True)
                time.sleep(1)
            time.sleep(1)
        
        # 베팅이 안 되었을 경우 강제 재시작
        st.warning("베팅 시간이 종료되었습니다! 다음 라운드를 기다려주세요.")
        time.sleep(2)
        st.rerun()

    else:
        # 베팅 완료 후 카드 오픈 연출
        timer_placeholder.markdown("<p class='timer-text' style='text-align:center; color:#f1c40f;'>DEALING...</p>", unsafe_allow_html=True)
        
        # 카드 셔플
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
        
        with card_col1:
            st.markdown(f"<h3 style='text-align:center; color:#e74c3c;'>PLAYER</h3>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align:center;'>{' '.join(p_hand)}</h1>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align:center;'>{ps}</h2>", unsafe_allow_html=True)
        with card_col2:
            st.markdown(f"<h3 style='text-align:center; color:#3498db;'>BANKER</h3>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align:center;'>{' '.join(b_hand)}</h1>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align:center;'>{bs}</h2>", unsafe_allow_html=True)

        # 결과 판정
        res = "T" if ps == bs else ("P" if ps > bs else "B")
        st.session_state.history.append(res)
        
        if (st.session_state.bet_placed == "P" and res == "P"): st.session_state.balance += st.session_state.current_bet * 2; st.balloons()
        elif (st.session_state.bet_placed == "B" and res == "B"): st.session_state.balance += int(st.session_state.current_bet * 1.95); st.balloons()
        elif (st.session_state.bet_placed == "T" and res == "T"): st.session_state.balance += st.session_state.current_bet * 9; st.balloons()

        # 3초 뒤 초기화
        time.sleep(3)
        st.session_state.bet_placed = None
        st.rerun()

    # 5. 하단 고정 베팅 인터페이스 (사진 레이아웃)
    st.markdown("---")
    st.markdown(f"<h3 style='text-align:center;'>💰 자산: {st.session_state.balance:,}원</h3>", unsafe_allow_html=True)
    
    # 금액 선택 슬라이더
    bet_amount = st.select_slider("베팅 칩 선택", options=[1000, 5000, 10000, 50000, 100000], value=1000)

    b_col1, b_col2, b_col3 = st.columns(3)
    with b_col1:
        if st.button("👤 PLAYER\n2.0x", use_container_width=True):
            st.session_state.bet_placed = "P"
            st.session_state.current_bet = bet_amount
            st.session_state.balance -= bet_amount
            st.toast("플레이어 베팅 완료!")
    with b_col2:
        if st.button("👔 TIE\n9.0x", use_container_width=True):
            st.session_state.bet_placed = "T"
            st.session_state.current_bet = bet_amount
            st.session_state.balance -= bet_amount
            st.toast("타이 베팅 완료!")
    with b_col3:
        if st.button("🏦 BANKER\n1.95x", use_container_width=True, type="primary"):
            st.session_state.bet_placed = "B"
            st.session_state.current_bet = bet_amount
            st.session_state.balance -= bet_amount
            st.toast("뱅커 베팅 완료!")