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

dealer_base64 = get_base64_img("game/dealer.jpg") #

# 3. 게임 상태 초기화
if 'game_started' not in st.session_state: st.session_state.game_started = False
if 'balance' not in st.session_state: st.session_state.balance = 100000
if 'history' not in st.session_state: st.session_state.history = []
if 'bet_placed' not in st.session_state: st.session_state.bet_placed = None

# --- [스테이지 1: 인트로 영상 & 실행 버튼] ---
if not st.session_state.game_started:
    st.markdown("<h1 style='text-align:center; color:white;'>JAEGUK LIVE CASINO</h1>", unsafe_allow_html=True)
    try: 
        st.video("game/intro.mp4") #
    except: 
        st.warning("인트로 영상 파일(game/intro.mp4)을 확인해주세요.")
    
    # 카지노 입장 버튼
    if st.button("🧧 라이브 스튜디오 입장 (BGM ON)", use_container_width=True):
        st.session_state.game_started = True
        st.rerun()

# --- [스테이지 2: 메인 게임 스튜디오] ---
else:
    # 핵심 CSS: 사진 사이즈 조절, 잔액 위치, 버튼 레이어 고정
    st.markdown(f"""
        <style>
        [data-testid="stAppViewContainer"] {{ overflow: hidden !important; background-color: #000; }}
        [data-testid="stHeader"] {{ display: none; }}
        
        /* 1. 빨간 테이블 배경 */
        .casino-bg {{
            position: fixed; top: 0; left: 0; width: 100%; height: 780px;
            background: radial-gradient(circle, #d32f2f 0%, #1a0000 100%);
            border-bottom: 15px solid #3d2b1f; border-radius: 0 0 50% 50% / 0 0 10% 10%;
            z-index: 1;
        }}
        /* 2. 딜러 사진 (사이즈 줄이고 글자 위로 배치) */
        .dealer-photo {{
            position: fixed; top: 15px; left: 50%; transform: translateX(-50%);
            width: 160px; /* 글자랑 안 겹치게 사이즈 최적화 */
            border: 3px solid #fbbf24; border-radius: 12px;
            z-index: 10; box-shadow: 0 0 20px rgba(251, 191, 36, 0.5);
        }}
        /* 3. 베팅하세요 글자 */
        .status-ui {{
            position: fixed; top: 195px; left: 50%; transform: translateX(-50%);
            width: 100%; text-align: center; font-size: 52px; font-weight: bold;
            color: #fbbf24; text-shadow: 3px 3px 10px #000; z-index: 20;
        }}
        /* 4. 잔액 글자 (베팅하세요 바로 밑에 크게) */
        .balance-ui {{
            position: fixed; top: 275px; left: 50%; transform: translateX(-50%);
            width: 100%; text-align: center; font-size: 45px; font-weight: bold;
            color: #ffffff; text-shadow: 2px 2px 8px #000; z-index: 25;
        }}
        /* 5. 버튼 레이어 (테이블 위로 강제 고정) */
        div[data-testid="stHorizontalBlock"] {{
            position: fixed !important; top: 530px !important; left: 50% !important;
            transform: translateX(-50%) !important; width: 85% !important; z-index: 1000 !important;
        }}
        .stButton > button {{
            background-color: rgba(0, 0, 0, 0.7) !important;
            color: white !important; border: 2px solid #fbbf24 !important;
            height: 95px !important; font-size: 26px !important; font-weight: bold !important;
            border-radius: 15px !important;
        }}
        </style>
        
        <div class="casino-bg"></div>
        <img src="data:image/jpg;base64,{dealer_base64}" class="dealer-photo">
    """, unsafe_allow_html=True)

    # 사운드 강제 재생
    st.components.v1.html("""
        <iframe width="0" height="0" src="https://www.youtube.com/embed/fZZS8GZStUw?autoplay=1&loop=1&playlist=fZZS8GZStUw" 
        frameborder="0" allow="autoplay"></iframe>
    """, height=0)

    msg_placeholder = st.empty()
    bal_placeholder = st.empty()

    # --- 베팅 UI 실행 ---
    if st.session_state.bet_placed is None:
        # 잔액 표시
        bal_placeholder.markdown(f"<div class='balance-ui'>💰 잔액: {st.session_state.balance:,}원</div>", unsafe_allow_html=True)
        
        # 베팅 버튼 (테이블 곡선 위 정중앙)
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("👤 PLAYER", use_container_width=True):
                st.session_state.bet_placed = "P"; st.rerun()
        with c2:
            if st.button("👔 TIE", use_container_width=True):
                st.session_state.bet_placed = "T"; st.rerun()
        with c3:
            if st.button("🏦 BANKER", use_container_width=True):
                st.session_state.bet_placed = "B"; st.rerun()

        # 베팅 대기 타이머
        for i in range(15, -1, -1):
            msg_placeholder.markdown(f"<div class='status-ui'>베팅하세요: {i}초</div>", unsafe_allow_html=True)
            time.sleep(1)
        st.rerun()
    else:
        # 게임 연출 및 승패 로직 (이후 카드 애니메이션 등 추가 가능)
        st.session_state.balance -= 10000
        msg_placeholder.markdown("<div class='status-ui' style='color:#ff5252;'>베팅 마감!</div>", unsafe_allow_html=True)
        bal_placeholder.empty()
        time.sleep(2)
        st.session_state.bet_placed = None
        st.rerun()