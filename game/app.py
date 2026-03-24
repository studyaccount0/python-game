import streamlit as st
import random
import time
import base64

# 1. 페이지 설정 및 강제 스크롤 차단
st.set_page_config(page_title="재국 라이브 스튜디오", page_icon="🎰", layout="wide")

# 2. 이미지 베이스64 (사진이 안 깨지게 만드는 가장 확실한 방법)
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
if 'bet_amount' not in st.session_state: st.session_state.bet_amount = 0

# --- [스테이지 1: 인트로 영상] ---
if not st.session_state.game_started:
    st.markdown("<h1 style='text-align:center; color:white; font-family:sans-serif;'>JAEGUK LIVE CASINO</h1>", unsafe_allow_html=True)
    try:
        st.video("game/intro.mp4") #
    except:
        st.warning("인트로 영상을 준비 중입니다...")
    
    if st.button("🧧 라이브 스튜디오 입장 (BGM ON)", use_container_width=True):
        st.session_state.game_started = True
        st.rerun()

# --- [스테이지 2: 메인 게임 스튜디오] ---
else:
    # 핵심 CSS: 테이블 사이즈 확대, 사진/글자 겹치기, 스크롤 완전 차단
    st.markdown(f"""
        <style>
        /* 전체 화면 스크롤 금지 */
        [data-testid="stAppViewContainer"] {{ overflow: hidden !important; background-color: #000; }}
        [data-testid="stHeader"] {{ display: none; }}
        
        /* 1. 빨간 테이블 (배경 고정 및 사이즈 확대) */
        .casino-background {{
            position: fixed; top: 0; left: 0; width: 100%; height: 620px;
            background: radial-gradient(circle, #d32f2f 0%, #2b0000 100%);
            border-bottom: 12px solid #3d2b1f; border-radius: 0 0 50% 50% / 0 0 12% 12%;
            z-index: 1;
        }}
        /* 2. 딜러 사진 (테이블 위 중앙 고정) */
        .dealer-photo {{
            position: fixed; top: 35px; left: 50%; transform: translateX(-50%);
            width: 240px; border: 5px solid #fbbf24; border-radius: 18px;
            z-index: 10; box-shadow: 0 0 40px rgba(251, 191, 36, 0.6);
        }}
        /* 3. 상태 안내 글자 (딜러 사진 아래 중앙 고정) */
        .status-msg {{
            position: fixed; top: 320px; left: 50%; transform: translateX(-50%);
            width: 100%; text-align: center; font-size: 65px; font-weight: bold;
            color: #fbbf24; text-shadow: 3px 3px 15px #000; z-index: 20;
        }}
        /* 4. 카드 애니메이션 */
        .card-anim {{
            font-size: 95px; display: inline-block; margin: 15px;
            filter: drop-shadow(5px 5px 12px rgba(0,0,0,0.6));
            animation: card-deal 0.9s cubic-bezier(0.25, 1, 0.5, 1) forwards;
        }}
        @keyframes card-deal {{
            0% {{ transform: translate(-500px, -250px) rotate(-200deg) scale(0); opacity: 0; }}
            100% {{ transform: translate(0, 0) rotate(0deg) scale(1); opacity: 1; }}
        }}
        /* 베팅 버튼 스타일 */
        .stButton > button {{ z-index: 100 !important; height: 85px !important; font-size: 24px !important; font-weight: bold !important; }}
        </style>
        
        <div class="casino-background"></div>
        <img src="data:image/jpg;base64,{dealer_base64}" class="dealer-photo">
    """, unsafe_allow_html=True)

    # 사운드 시스템 (유튜브 API 활용 긴장감 흐르는 BGM)
    st.components.v1.html("""
        <iframe width="0" height="0" src="https://www.youtube.com/embed/fZZS8GZStUw?autoplay=1&loop=1&playlist=fZZS8GZStUw" 
        frameborder="0" allow="autoplay"></iframe>
    """, height=0)

    msg_box = st.empty()
    card_box = st.empty()

    # 테이블 아래 베팅 구역 확보 (여백)
    st.markdown("<br>" * 23, unsafe_allow_html=True)
    
    # 베팅 UI (플레이어, 타이, 뱅커 버튼 노출)
    if st.session_state.bet_placed is None:
        st.markdown(f"<h2 style='text-align:center; color:white;'>💰 현재 잔액: {st.session_state.balance:,}원</h2>", unsafe_allow_html=True)
        bet_amt = st.select_slider("베팅 금액 선택", options=[1000, 5000, 10000, 50000, 100000, 500000], value=10000)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("👤 PLAYER (2.0x)", use_container_width=True):
                st.session_state.bet_placed = "P"; st.session_state.bet_amount = bet_amt; st.rerun()
        with col2:
            if st.button("👔 TIE (9.0x)", use_container_width=True):
                st.session_state.bet_placed = "T"; st.session_state.bet_amount = bet_amt; st.rerun()
        with col3:
            if st.button("🏦 BANKER (1.95x)", use_container_width=True, type="primary"):
                st.session_state.bet_placed = "B"; st.session_state.bet_amount = bet_amt; st.rerun()

        # 15초 실시간 타이머 (중앙 고정)
        for i in range(15, -1, -1):
            msg_box.markdown(f"<div class='status-msg'>베팅하세요: {i}초</div>", unsafe_allow_html=True)
            time.sleep(1)
        st.rerun()

    else:
        # 게임 진행 연출 (카드 딜링)
        st.session_state.balance -= st.session_state.bet_amount
        msg_box.markdown("<div class='status-msg' style='color:#ff5252;'>베팅 마감 (NO MORE BETS)</div>", unsafe_allow_html=True)
        time.sleep(2)

        deck = [f"{s}{r}" for s in ['♠️','♥️','♣️','♦️'] for r in ['A','2','3','4','5','6','7','8','9','10','J','Q','K']]
        random.shuffle(deck)
        p_h, b_h = [deck.pop(), deck.pop()], [deck.pop(), deck.pop()]
        
        def score(h):
            s = sum([1 if c[2:]=='A' else (0 if c[2:] in ['10','J','Q','K'] else int(c[2:])) for c in h])
            return s % 10

        ps, bs = score(p_h), score(b_h)

        # 딜링 애니메이션 (카드 한 장씩 날아옴)
        msg_box.empty()
        p_v, b_v = [], []
        for i in range(2):
            p_v.append(p_h[i])
            card_box.markdown(f"""
                <div style='position:fixed; top:400px; left:50%; transform:translateX(-50%); display:flex; gap:110px; z-index:100;'>
                    <div class='card-anim' style='color:#ff5252;'>P<br>{' '.join(p_v)}</div>
                    <div class='card-anim' style='color:#448aff;'>B<br>{' '.join(b_v)}</div>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(3.5)
            
            b_v.append(b_h[i])
            card_box.markdown(f"""
                <div style='position:fixed; top:400px; left:50%; transform:translateX(-50%); display:flex; gap:110px; z-index:100;'>
                    <div class='card-anim' style='color:#ff5252;'>P<br>{' '.join(p_v)}</div>
                    <div class='card-anim' style='color:#448aff;'>B<br>{' '.join(b_v)}</div>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(3.5)

        # 승패 결과 확인
        res = "T" if ps == bs else ("P" if ps > bs else "B")
        st.session_state.history.append(res)
        
        if (st.session_state.bet_placed == res):
            mult = 9 if res=="T" else (2 if res=="P" else 1.95)
            win = int(st.session_state.bet_amount * mult)
            st.session_state.balance += win
            st.balloons()
            msg_box.markdown(f"<div class='status-msg' style='color:#4caf50;'>🎉 {win:,}원 당첨! (총액: {st.session_state.balance:,}원)</div>", unsafe_allow_html=True)
        else:
            msg_box.markdown("<div class='status-msg' style='color:#9e9e9e;'>낙첨되었습니다.</div>", unsafe_allow_html=True)
        
        time.sleep(4)
        st.session_state.bet_placed = None
        st.rerun()

    # 기록지
    road_html = "<div style='position:fixed; bottom:20px; right:20px; display:grid; grid-template-columns:repeat(6,25px); gap:5px; background:rgba(0,0,0,0.8); padding:10px; border-radius:10px; z-index:150;'>"
    for r in st.session_state.history[-36:]:
        c = "#ff5252" if r == "P" else ("#448aff" if r == "B" else "#4caf50")
        road_html += f"<div style='width:22px; height:22px; background:{c}; border-radius:50%; color:white; font-size:11px; text-align:center; line-height:22px; font-weight:bold;'>{r}</div>"
    road_html += "</div>"
    st.markdown(road_html, unsafe_allow_html=True)