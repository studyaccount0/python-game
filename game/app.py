import streamlit as st
import random
import time
import base64

# 1. 페이지 설정 및 스크롤 차단
st.set_page_config(page_title="재국 라이브 스튜디오", page_icon="🎰", layout="wide")

# 2. 이미지 베이스64 (딜러 사진)
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

# --- [스테이지 1: 인트로 영상 & 실행 버튼] ---
if not st.session_state.game_started:
    st.markdown("<h1 style='text-align:center; color:white;'>JAEGUK LIVE CASINO</h1>", unsafe_allow_html=True)
    try: st.video("game/intro.mp4")
    except: st.warning("인트로 영상을 확인해주세요.")
    
    if st.button("🧧 라이브 스튜디오 입장 (BGM ON)", use_container_width=True):
        st.session_state.game_started = True
        st.rerun()

# --- [스테이지 2: 메인 게임 스튜디오] ---
else:
    # 핵심 CSS: 카드 개별 애니메이션 추가
    st.markdown(f"""
        <style>
        [data-testid="stAppViewContainer"] {{ overflow: hidden !important; background-color: #000; }}
        [data-testid="stHeader"] {{ display: none; }}
        
        .casino-bg {{
            position: fixed; top: 0; left: 0; width: 100%; height: 780px;
            background: radial-gradient(circle, #d32f2f 0%, #1a0000 100%);
            border-bottom: 15px solid #3d2b1f; border-radius: 0 0 50% 50% / 0 0 10% 10%;
            z-index: 1;
        }}
        .dealer-photo {{
            position: fixed; top: 15px; left: 50%; transform: translateX(-50%);
            width: 160px; border: 3px solid #fbbf24; border-radius: 12px;
            z-index: 10; box-shadow: 0 0 20px rgba(251, 191, 36, 0.5);
        }}
        .status-ui {{
            position: fixed; top: 195px; left: 50%; transform: translateX(-50%);
            width: 100%; text-align: center; font-size: 52px; font-weight: bold;
            color: #fbbf24; text-shadow: 3px 3px 10px #000; z-index: 20;
        }}
        .balance-ui {{
            position: fixed; top: 275px; left: 50%; transform: translateX(-50%);
            width: 100%; text-align: center; font-size: 45px; font-weight: bold;
            color: #ffffff; text-shadow: 2px 2px 8px #000; z-index: 25;
        }}
        
        /* 카드 구역 및 애니메이션 (모든 카드에 적용) */
        .card-container {{
            position: fixed; top: 350px; left: 50%; transform: translateX(-50%);
            display: flex; gap: 100px; z-index: 50;
        }}
        .card-box {{ font-size: 80px; text-align: center; font-weight: bold; }}
        
        .card-anim {{
            display: inline-block;
            animation: deal-card 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
            filter: drop-shadow(5px 5px 10px rgba(0,0,0,0.5));
        }}
        
        @keyframes deal-card {{
            0% {{ transform: translate(300px, -300px) rotate(180deg) scale(0); opacity: 0; }}
            100% {{ transform: translate(0, 0) rotate(0deg) scale(1); opacity: 1; }}
        }}

        div[data-testid="stHorizontalBlock"] {{
            position: fixed !important; top: 550px !important; left: 50% !important;
            transform: translateX(-50%) !important; width: 85% !important; z-index: 1000 !important;
        }}
        .stButton > button {{
            background-color: rgba(0, 0, 0, 0.7) !important;
            color: white !important; border: 2px solid #fbbf24 !important;
            height: 80px !important; font-size: 24px !important; font-weight: bold !important;
        }}
        </style>
        
        <div class="casino-bg"></div>
        <img src="data:image/jpg;base64,{dealer_base64}" class="dealer-photo">
    """, unsafe_allow_html=True)

    # 사운드 실행
    st.components.v1.html("""<iframe width="0" height="0" src="https://www.youtube.com/embed/fZZS8GZStUw?autoplay=1&loop=1&playlist=fZZS8GZStUw" frameborder="0" allow="autoplay"></iframe>""", height=0)

    msg_holder = st.empty()
    bal_holder = st.empty()
    card_holder = st.empty()

    if st.session_state.bet_placed is None:
        bal_placeholder_text = f"<div class='balance-ui'>💰 잔액: {st.session_state.balance:,}원</div>"
        bal_holder.markdown(bal_placeholder_text, unsafe_allow_html=True)
        
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

        for i in range(15, -1, -1):
            msg_holder.markdown(f"<div class='status-ui'>베팅하세요: {i}초</div>", unsafe_allow_html=True)
            time.sleep(1)
        st.rerun()
    else:
        # 카드 딜링 시작
        st.session_state.balance -= 10000
        msg_holder.markdown("<div class='status-ui' style='color:#ff5252;'>베팅 마감!</div>", unsafe_allow_html=True)
        time.sleep(1)

        # 덱 생성 및 카드 결정
        deck = [f"{s}{r}" for s in ['♠️','♥️','♣️','♦️'] for r in ['A','2','3','4','5','6','7','8','9','10','J','Q','K']]
        random.shuffle(deck)
        p_cards = [deck.pop(), deck.pop()]
        b_cards = [deck.pop(), deck.pop()]

        # 카드 한 장씩 애니메이션과 함께 노출 (총 4번의 애니메이션)
        current_p = []
        current_b = []
        
        for i in range(2):
            # 플레이어 카드 딜링
            current_p.append(p_cards[i])
            p_html = "".join([f"<span class='card-anim'>{c}</span>" for c in current_p])
            b_html = "".join([f"<span class='card-anim'>{c}</span>" for c in current_b])
            card_holder.markdown(f"<div class='card-container'><div class='card-box' style='color:#ff5252;'>P<br>{p_html}</div><div class='card-box' style='color:#448aff;'>B<br>{b_html}</div></div>", unsafe_allow_html=True)
            time.sleep(1.2) # 카드 날아오는 시간

            # 뱅커 카드 딜링
            current_b.append(b_cards[i])
            p_html = "".join([f"<span class='card-anim'>{c}</span>" for c in current_p])
            b_html = "".join([f"<span class='card-anim'>{c}</span>" for c in current_b])
            card_holder.markdown(f"<div class='card-container'><div class='card-box' style='color:#ff5252;'>P<br>{p_html}</div><div class='card-box' style='color:#448aff;'>B<br>{b_html}</div></div>", unsafe_allow_html=True)
            time.sleep(1.2)

        # 결과 계산
        def get_score(h):
            return sum([1 if c[2:]=='A' else (0 if c[2:] in ['10','J','Q','K'] else int(c[2:])) for c in h]) % 10
        ps, bs = get_score(p_cards), get_score(b_cards)
        res = "T" if ps == bs else ("P" if ps > bs else "B")
        
        if st.session_state.bet_placed == res:
            st.balloons()
            msg_holder.markdown(f"<div class='status-ui' style='color:#4caf50;'>WIN! (Score {ps}:{bs})</div>", unsafe_allow_html=True)
            st.session_state.balance += 20000
        else:
            msg_placeholder_text = f"<div class='status-ui' style='color:#9e9e9e;'>LOSE (Score {ps}:{bs})</div>"
            msg_holder.markdown(msg_placeholder_text, unsafe_allow_html=True)
        
        time.sleep(4)
        st.session_state.bet_placed = None
        st.rerun()