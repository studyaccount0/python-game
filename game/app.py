import streamlit as st
import random
import time
import base64

# 1. 페이지 설정 및 스크롤 완전 차단
st.set_page_config(page_title="재국 라이브 스튜디오", page_icon="🎰", layout="wide")

# 2. 이미지 베이스64 (딜러 사진 고정)
def get_base64_img(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except: return ""

dealer_base64 = get_base64_img("game/dealer.jpg")

# 3. 게임 상태 초기화
if 'game_started' not in st.session_state: st.session_state.game_started = False
if 'balance' not in st.session_state: st.session_state.balance = 100000
if 'history' not in st.session_state: st.session_state.history = []
if 'bet_placed' not in st.session_state: st.session_state.bet_placed = None
if 'bet_amount' not in st.session_state: st.session_state.bet_amount = 0

# --- [스테이지 1: 인트로 영상] ---
if not st.session_state.game_started:
    st.markdown("<h1 style='text-align:center; color:white;'>JAEGUK LIVE CASINO</h1>", unsafe_allow_html=True)
    try: st.video("game/intro.mp4")
    except: st.warning("인트로 영상 로딩 중...")
    if st.button("🧧 라이브 스튜디오 입장 (BGM ON)", use_container_width=True):
        st.session_state.game_started = True
        st.rerun()

# --- [스테이지 2: 메인 게임 스튜디오] ---
else:
    # 핵심 CSS: 모든 요소를 레이어 순서대로 강제 배치
    st.markdown(f"""
        <style>
        [data-testid="stAppViewContainer"] {{ overflow: hidden !important; background-color: #000; }}
        [data-testid="stHeader"] {{ display: none; }}
        
        /* 1. 빨간 테이블 (배경) */
        .casino-bg {{
            position: fixed; top: 0; left: 0; width: 100%; height: 750px;
            background: radial-gradient(circle, #d32f2f 0%, #1a0000 100%);
            border-bottom: 15px solid #3d2b1f; border-radius: 0 0 50% 50% / 0 0 10% 10%;
            z-index: 1;
        }}
        /* 2. 딜러 사진 (글자 위까지만 오도록 위치 조정) */
        .dealer-photo {{
            position: fixed; top: 20px; left: 50%; transform: translateX(-50%);
            width: 200px; border: 4px solid #fbbf24; border-radius: 12px;
            z-index: 10; box-shadow: 0 0 30px rgba(251, 191, 36, 0.5);
        }}
        /* 3. 상태 안내 (베팅하세요) */
        .status-ui {{
            position: fixed; top: 250px; left: 50%; transform: translateX(-50%);
            width: 100%; text-align: center; font-size: 55px; font-weight: bold;
            color: #fbbf24; text-shadow: 3px 3px 10px #000; z-index: 20;
        }}
        /* 4. 카드 애니메이션 */
        .card-area {{
            position: fixed; top: 340px; left: 50%; transform: translateX(-50%);
            display: flex; gap: 80px; z-index: 30;
        }}
        .card-anim {{
            font-size: 85px; filter: drop-shadow(5px 5px 10px rgba(0,0,0,0.6));
            animation: deal 0.8s ease-out forwards;
        }}
        @keyframes deal {{
            0% {{ transform: translateY(-200px) rotate(-180deg) scale(0); opacity: 0; }}
            100% {{ transform: translateY(0) rotate(0deg) scale(1); opacity: 1; }}
        }}
        
        /* 5. 버튼 구역 (테이블 중앙에 칩처럼 배치) */
        .betting-buttons {{
            position: fixed; top: 520px; left: 50%; transform: translateX(-50%);
            display: flex; gap: 20px; z-index: 100;
        }}
        /* 스트림릿 버튼 강제 스타일링 */
        div[data-testid="stHorizontalBlock"] {{
            position: fixed !important; top: 520px !important; left: 50% !important;
            transform: translateX(-50%) !important; width: 80% !important; z-index: 1000 !important;
        }}
        .stButton > button {{
            background-color: rgba(255, 255, 255, 0.1) !important;
            color: white !important; border: 2px solid #fbbf24 !important;
            height: 80px !important; font-size: 22px !important; font-weight: bold !important;
            box-shadow: 0 5px 15px rgba(0,0,0,0.5) !important;
        }}
        </style>
        
        <div class="casino-bg"></div>
        <img src="data:image/jpg;base64,{dealer_base64}" class="dealer-photo">
    """, unsafe_allow_html=True)

    # 사운드 시스템
    st.components.v1.html("""
        <iframe width="0" height="0" src="https://www.youtube.com/embed/fZZS8GZStUw?autoplay=1&loop=1&playlist=fZZS8GZStUw" 
        frameborder="0" allow="autoplay"></iframe>
    """, height=0)

    msg_placeholder = st.empty()
    card_placeholder = st.empty()

    # --- [베팅 구역: 테이블 정중앙 위로 강제 배치] ---
    if st.session_state.bet_placed is None:
        st.markdown(f"<div style='position:fixed; top:460px; width:100%; text-align:center; color:white; z-index:100;'>💰 잔액: {st.session_state.balance:,}원</div>", unsafe_allow_html=True)
        
        # 버튼을 감싸는 컬럼 (z-index 1000으로 테이블 위로 띄움)
        bet_col = st.container()
        with bet_col:
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("👤 PLAYER", use_container_width=True):
                    st.session_state.bet_placed = "P"; st.session_state.bet_amount = 10000; st.rerun()
            with c2:
                if st.button("👔 TIE", use_container_width=True):
                    st.session_state.bet_placed = "T"; st.session_state.bet_amount = 10000; st.rerun()
            with c3:
                if st.button("🏦 BANKER", use_container_width=True):
                    st.session_state.bet_placed = "B"; st.session_state.bet_amount = 10000; st.rerun()

        for i in range(15, -1, -1):
            msg_placeholder.markdown(f"<div class='status-ui'>베팅하세요: {i}초</div>", unsafe_allow_html=True)
            time.sleep(1)
        st.rerun()
    else:
        # 게임 연출 및 결과 (기존 로직 유지)
        st.session_state.balance -= st.session_state.bet_amount
        msg_placeholder.markdown("<div class='status-ui' style='color:#ff5252;'>베팅 마감!</div>", unsafe_allow_html=True)
        time.sleep(2)

        deck = [f"{s}{r}" for s in ['♠️','♥️','♣️','♦️'] for r in ['A','2','3','4','5','6','7','8','9','10','J','Q','K']]
        random.shuffle(deck)
        p_h, b_h = [deck.pop(), deck.pop()], [deck.pop(), deck.pop()]
        ps = sum([1 if c[2:]=='A' else (0 if c[2:] in ['10','J','Q','K'] else int(c[2:])) for c in p_h]) % 10
        bs = sum([1 if c[2:]=='A' else (0 if c[2:] in ['10','J','Q','K'] else int(c[2:])) for c in b_h]) % 10

        p_v, b_v = [], []
        for i in range(2):
            p_v.append(p_h[i]); b_v.append(b_h[i])
            card_placeholder.markdown(f"""<div class='card-area'><div class='card-anim' style='color:#ff5252;'>P<br>{' '.join(p_v)}</div><div class='card-anim' style='color:#448aff;'>B<br>{' '.join(b_v)}</div></div>""", unsafe_allow_html=True)
            time.sleep(3.5)

        res = "T" if ps == bs else ("P" if ps > bs else "B")
        st.session_state.history.append(res)
        if st.session_state.bet_placed == res:
            st.balloons()
            msg_placeholder.markdown(f"<div class='status-ui' style='color:#4caf50;'>🎉 당첨!</div>", unsafe_allow_html=True)
        else:
            msg_placeholder.markdown("<div class='status-ui' style='color:#9e9e9e;'>낙첨되었습니다.</div>", unsafe_allow_html=True)
        
        time.sleep(4); st.session_state.bet_placed = None; st.rerun()