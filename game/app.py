import streamlit as st
import random
import time

# 1. 페이지 설정
st.set_page_config(page_title="재국 라이브 스튜디오", page_icon="🎰", layout="wide")

# 2. 게임 상태 초기화
if 'balance' not in st.session_state: st.session_state.balance = 100000
if 'history' not in st.session_state: st.session_state.history = []
if 'game_started' not in st.session_state: st.session_state.game_started = False
if 'bet_placed' not in st.session_state: st.session_state.bet_placed = None
if 'bet_amount' not in st.session_state: st.session_state.bet_amount = 0

# 3. 레이아웃 겹치기 및 스타일 (이미지 위에 글자/사진 배치)
st.markdown("""
    <style>
    .main { background-color: #000; color: white; }
    
    /* 상단 빨간 테이블 영역 (배경) */
    .casino-header {
        position: relative;
        background: radial-gradient(circle, #e63946 0%, #300000 100%);
        height: 550px;
        border-radius: 0 0 50% 50% / 0 0 15% 15%;
        border-bottom: 8px solid #4e342e;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 0 15px 40px rgba(0,0,0,0.9);
        z-index: 1;
        margin-bottom: 20px;
    }

    /* 딜러 이미지: 글자 위에 오도록 배치 */
    .dealer-img-box {
        position: absolute;
        top: 30px;
        border: 4px solid #ffca28;
        border-radius: 15px;
        box-shadow: 0 0 25px rgba(255, 202, 40, 0.5);
        z-index: 100 !important;
    }

    /* 상태 텍스트: 배경 위, 딜러 아래 */
    .status-overlay {
        position: relative;
        top: 120px;
        font-size: 60px;
        font-weight: bold;
        color: #ffca28;
        text-shadow: 0 0 20px rgba(255, 202, 40, 0.8);
        z-index: 10;
        text-align: center;
    }

    /* 카드 애니메이션 */
    .card-anim {
        font-size: 90px; display: inline-block; margin: 15px;
        animation: deal-card 0.8s ease-out forwards;
    }
    @keyframes deal-card {
        0% { transform: translateY(-200px) rotate(180deg) scale(0); opacity: 0; }
        100% { transform: translateY(0) rotate(0deg) scale(1); opacity: 1; }
    }

    /* 하단 버튼 및 슬라이더 스타일 */
    .stSlider { padding: 20px 50px; }
    .stButton>button { height: 100px !important; font-size: 25px !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. 음악 자동 재생 (YouTube API 사용 - 루프 및 자동재생 강제)
# 음악이 안 들리면 화면 아무 곳이나 한 번 클릭해 주세요!
st.components.v1.html("""
    <iframe width="0" height="0" src="https://www.youtube.com/embed/fZZS8GZStUw?autoplay=1&loop=1&playlist=fZZS8GZStUw&mute=0" 
    frameborder="0" allow="autoplay"></iframe>
""", height=0)

# --- [인트로 화면] ---
if not st.session_state.game_started:
    try:
        st.video("game/intro.mp4")
    except:
        st.error("비디오 파일을 찾을 수 없습니다.")
    
    if st.button("🔥 카지노 입장하기 (클릭 시 음악 재생 시작)", use_container_width=True):
        st.session_state.game_started = True
        st.rerun()

# --- [메인 게임 화면] ---
else:
    # 1. 상단: 겹쳐진 레이아웃 (배경 + 딜러 + 텍스트)
    st.markdown("<div class='casino-header'>", unsafe_allow_html=True)
    
    # 딜러 사진 (상단 중앙)
    c1, c2, c3 = st.columns([1, 0.8, 1])
    with c2:
        try:
            st.markdown("<div class='dealer-img-box'>", unsafe_allow_html=True)
            st.image("game/dealer.jpg", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        except:
            st.write("👤 [딜러 입장 전]")
            
    # 상태 텍스트 공간
    msg_box = st.empty()
    card_box = st.empty()
    st.markdown("</div>", unsafe_allow_html=True)

    # 2. 잔액 표시
    st.markdown(f"<h1 style='text-align:center;'>💰 현재 잔액: {st.session_state.balance:,}원</h1>", unsafe_allow_html=True)

    # 3. 게임 로직 (베팅 15초)
    if st.session_state.bet_placed is None:
        st.write("---")
        bet_amt = st.select_slider("베팅 칩 금액을 선택하세요", options=[1000, 5000, 10000, 50000, 100000, 500000], value=10000)
        
        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("플레이어 (2.0x)", use_container_width=True):
                st.session_state.bet_placed = "P"; st.session_state.bet_amount = bet_amt; st.rerun()
        with b2:
            if st.button("타이 (9.0x)", use_container_width=True):
                st.session_state.bet_placed = "T"; st.session_state.bet_amount = bet_amt; st.rerun()
        with b3:
            if st.button("뱅커 (1.95x)", use_container_width=True, type="primary"):
                st.session_state.bet_placed = "B"; st.session_state.bet_amount = bet_amt; st.rerun()

        for i in range(15, -1, -1):
            msg_box.markdown(f"<div class='status-overlay'>베팅하세요: {i}초</div>", unsafe_allow_html=True)
            time.sleep(1)
        st.rerun()

    else:
        # 베팅 종료 후 딜링 (15초 연출)
        st.session_state.balance -= st.session_state.bet_amount
        msg_box.markdown("<div class='status-overlay' style='color:#ff4d4d;'>베팅 종료!</div>", unsafe_allow_html=True)
        time.sleep(2)

        deck = [f"{s}{r}" for s in ['♠️','♥️','♣️','♦️'] for r in ['A','2','3','4','5','6','7','8','9','10','J','Q','K']]
        random.shuffle(deck)
        p_h, b_h = [deck.pop(), deck.pop()], [deck.pop(), deck.pop()]
        
        def score(h):
            s = sum([1 if c[2:]=='A' else (0 if c[2:] in ['10','J','Q','K'] else int(c[2:])) for c in h])
            return s % 10

        ps, bs = score(p_h), score(b_h)

        # 카드 딜링 애니메이션
        msg_box.empty()
        p_now, b_now = [], []
        for i in range(2):
            p_now.append(p_h[i])
            card_box.markdown(f"""
                <div style='display:flex; justify-content:center; gap:120px; margin-top:220px;'>
                    <div class='card-anim' style='color:#e63946;'>P<br>{' '.join(p_now)}</div>
                    <div class='card-anim' style='color:#3498db;'>B<br>{' '.join(b_now)}</div>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(3.5)
            
            b_now.append(b_h[i])
            card_box.markdown(f"""
                <div style='display:flex; justify-content:center; gap:120px; margin-top:220px;'>
                    <div class='card-anim' style='color:#e63946;'>P<br>{' '.join(p_now)}</div>
                    <div class='card-anim' style='color:#3498db;'>B<br>{' '.join(b_now)}</div>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(3.5)

        # 결과 확인
        res = "T" if ps == bs else ("P" if ps > bs else "B")
        st.session_state.history.append(res)
        
        win_money = 0
        if (st.session_state.bet_placed == "P" and res == "P"): win_money = st.session_state.bet_amount * 2
        elif (st.session_state.bet_placed == "B" and res == "B"): win_money = int(st.session_state.bet_amount * 1.95)
        elif (st.session_state.bet_placed == "T" and res == "T"): win_money = st.session_state.bet_amount * 9
        
        if win_money > 0:
            st.session_state.balance += win_money
            st.balloons()
            msg_box.markdown(f"<div class='status-overlay' style='color:#00ff00;'>🎊 {win_money:,}원 당첨!</div>", unsafe_allow_html=True)
        else:
            msg_box.markdown(f"<div class='status-overlay' style='color:#aaaaaa;'>낙첨되었습니다.</div>", unsafe_allow_html=True)
        
        time.sleep(4)
        st.session_state.bet_placed = None
        st.rerun()