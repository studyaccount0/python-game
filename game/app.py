import streamlit as st
import random
import time
import base64

# 1. 페이지 설정
st.set_page_config(page_title="재국 라이브 스튜디오", page_icon="🎰", layout="wide")

# 2. 이미지 처리 함수
def get_base64_img(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except: return ""

dealer_img = get_base64_img("game/dealer.jpg")

# 3. 세션 상태 초기화
if 'game_started' not in st.session_state: st.session_state.game_started = False
if 'balance' not in st.session_state: st.session_state.balance = 100000
if 'bet_placed' not in st.session_state: st.session_state.bet_placed = None
if 'bet_amount' not in st.session_state: st.session_state.bet_amount = 10000

# --- [스테이지 1: 인트로] ---
if not st.session_state.game_started:
    st.markdown("<h1 style='text-align:center; color:white;'>JAEGUK LIVE CASINO</h1>", unsafe_allow_html=True)
    try: 
        # 자동 재생(autoplay) 및 음소거(muted) 설정 추가
        st.video("game/intro.mp4", autoplay=True, muted=True)
    except: 
        st.warning("인트로 영상(game/intro.mp4)을 확인해주세요.")
    
    if st.button("🧧 라이브 스튜디오 입장", use_container_width=True):
        st.session_state.game_started = True
        st.rerun()

# --- [스테이지 2: 메인 게임] ---
else:
    # CSS 설정 (에러 방지를 위해 일반 문자열 처리)
    css_content = """
        <style>
        [data-testid="stAppViewContainer"] { overflow: hidden !important; background-color: #000; }
        [data-testid="stHeader"] { display: none; }
        
        /* 베팅 금액 슬라이더 위치 하향 조정 (310px -> 340px) */
        .stSlider {
            position: fixed !important; top: 340px !important; left: 50% !important;
            transform: translateX(-50%) !important; width: 350px !important; z-index: 100 !important;
        }
        
        .withdraw-info {
            position: fixed; top: 20px; left: 20px; padding: 12px;
            background: rgba(0,0,0,0.8); color: #fbbf24; border: 2px solid #fbbf24;
            border-radius: 10px; font-weight: bold; z-index: 100;
        }
        .casino-bg {
            position: fixed; top: 0; left: 0; width: 100%; height: 780px;
            background: radial-gradient(circle, #d32f2f 0%, #1a0000 100%);
            border-bottom: 15px solid #3d2b1f; border-radius: 0 0 50% 50% / 0 0 10% 10%;
            z-index: 1;
        }
        .dealer-photo {
            position: fixed; top: 15px; left: 50%; transform: translateX(-50%);
            width: 150px; border: 3px solid #fbbf24; border-radius: 12px;
            z-index: 10;
        }
        .status-ui {
            position: fixed; top: 180px; left: 50%; transform: translateX(-50%);
            width: 100%; text-align: center; font-size: 50px; font-weight: bold;
            color: #fbbf24; text-shadow: 2px 2px 10px #000; z-index: 20;
        }
        .balance-ui {
            position: fixed; top: 260px; left: 50%; transform: translateX(-50%);
            width: 100%; text-align: center; font-size: 40px; font-weight: bold;
            color: white; z-index: 25;
        }
        .card-container {
            position: fixed; top: 370px; left: 50%; transform: translateX(-50%);
            display: flex; gap: 80px; z-index: 50;
        }
        .card-box { font-size: 80px; text-align: center; font-weight: bold; }
        .card-anim {
            display: inline-block;
            animation: deal 1.2s cubic-bezier(0.175, 0.885, 0.32, 1) forwards;
        }
        @keyframes deal {
            0% { transform: translate(300px, -300px) scale(0); opacity: 0; }
            100% { transform: translate(0, 0) scale(1); opacity: 1; }
        }
        div[data-testid="stHorizontalBlock"] {
            position: fixed !important; top: 610px !important; left: 50% !important;
            transform: translateX(-50%) !important; width: 85% !important; z-index: 1000 !important;
        }
        .stButton > button {
            background-color: #111 !important; color: white !important;
            border: 2px solid #fbbf24 !important; height: 90px !important;
            font-size: 20px !important; border-radius: 15px !important;
        }
        </style>
        <div class="casino-bg"></div>
        <div class="withdraw-info">💰 100만원 달성 시 출금 가능</div>
    """
    st.markdown(css_content, unsafe_allow_html=True)

    if dealer_img:
        st.markdown('<img src="data:image/jpg;base64,' + dealer_img + '" class="dealer-photo">', unsafe_allow_html=True)

    st.components.v1.html('<iframe width="0" height="0" src="https://www.youtube.com/embed/fZZS8GZStUw?autoplay=1&loop=1&playlist=fZZS8GZStUw" frameborder="0" allow="autoplay"></iframe>', height=0)

    msg_h, bal_h, card_h = st.empty(), st.empty(), st.empty()

    if st.session_state.bet_placed is None:
        bal_h.markdown("<div class='balance-ui'>잔액: " + format(st.session_state.balance, ',') + "원</div>", unsafe_allow_html=True)
        
        m_bet = max(1000, st.session_state.balance)
        st.session_state.bet_amount = st.slider("BET", 1000, m_bet, value=min(st.session_state.bet_amount, m_bet), step=1000, label_visibility="collapsed")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("👤 플레이어\n(2.0x)", use_container_width=True):
                st.session_state.bet_placed = "P"; st.rerun()
        with c2:
            if st.button("👔 타이\n(8.0x)", use_container_width=True):
                st.session_state.bet_placed = "T"; st.rerun()
        with c3:
            if st.button("🏦 뱅커\n(1.95x)", use_container_width=True):
                st.session_state.bet_placed = "B"; st.rerun()

        for i in range(15, -1, -1):
            msg_h.markdown("<div class='status-ui'>베팅 시간: " + str(i) + "초</div>", unsafe_allow_html=True)
            time.sleep(1)
        st.rerun()
    else:
        now_bet = st.session_state.bet_amount
        st.session_state.balance -= now_bet
        msg_h.markdown("<div class='status-ui' style='color:#ff5252;'>베팅 마감!</div>", unsafe_allow_html=True)
        time.sleep(1)

        deck = [s + r for s in ['♠️','♥️','♣️','♦️'] for r in ['A','2','3','4','5','6','7','8','9','10','J','Q','K']]
        random.shuffle(deck)
        p_cards = [deck.pop(), deck.pop()]
        b_cards = [deck.pop(), deck.pop()]

        curr_p, curr_b = [], []
        for i in range(2):
            curr_p.append(p_cards[i])
            p_html = "".join(["<span class='card-anim'>" + c + "</span>" for c in curr_p])
            b_html = "".join(["<span class='card-anim'>" + c + "</span>" for c in curr_b])
            card_h.markdown("<div class='card-container'><div class='card-box' style='color:#ff5252;'>P<br>" + p_html + "</div><div class='card-box' style='color:#448aff;'>B<br>" + b_html + "</div></div>", unsafe_allow_html=True)
            time.sleep(1.2)

            curr_b.append(b_cards[i])
            p_html = "".join(["<span class='card-anim'>" + c + "</span>" for c in curr_p])
            b_html = "".join(["<span class='card-anim'>" + c + "</span>" for c in curr_b])
            card_h.markdown("<div class='card-container'><div class='card-box' style='color:#ff5252;'>P<br>" + p_html + "</div><div class='card-box' style='color:#448aff;'>B<br>" + b_html + "</div></div>", unsafe_allow_html=True)
            time.sleep(1.2)

        def score(h):
            s = 0
            for c in h:
                r = c[2:]
                if r == 'A': s += 1
                elif r in ['10','J','Q','K']: s += 0
                else: s += int(r)
            return s % 10
            
        ps, bs = score(p_cards), score(b_cards)
        win = "T" if ps == bs else ("P" if ps > bs else "B")
        
        if st.session_state.bet_placed == win:
            rate = 2.0 if win == "P" else (1.95 if win == "B" else 8.0)
            prize = int(now_bet * rate)
            st.session_state.balance += prize
            msg_h.markdown("<div class='status-ui' style='color:#4caf50;'>WIN! (+" + format(prize, ',') + "원)</div>", unsafe_allow_html=True)
        else:
            msg_h.markdown("<div class='status-ui' style='color:#9e9e9e;'>LOSE (" + str(ps) + ":" + str(bs) + ")</div>", unsafe_allow_html=True)
        
        time.sleep(3)
        st.session_state.bet_placed = None
        st.rerun()