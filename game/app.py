import streamlit as st
import random
import time
import base64

# 1. 페이지 설정 및 스크롤 완전 차단
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
    st.markdown(f"""
        <style>
        [data-testid="stAppViewContainer"] {{ overflow: hidden !important; background-color: #000; }}
        [data-testid="stHeader"] {{ display: none; }}
        
        .withdraw-info {{
            position: fixed; top: 20px; left: 20px;
            padding: 12px 18px; background: rgba(0, 0, 0, 0.75);
            color: #fbbf24; border: 2px solid #fbbf24; border-radius: 10px;
            font-size: 16px; font-weight: bold; z-index: 100;
            box-shadow: 0 0 15px rgba(251, 191, 36, 0.3);
            line-height: 1.4;
        }}

        .casino-bg {{
            position: fixed; top: 0; left: 0; width: 100%; height: 780px;
            background: radial-gradient(circle, #d32f2f 0%, #1a0000 100%);
            border-bottom: 15px solid #3d2b1f; border-radius: 0 0 50% / 0 0 10%;
            z-index: 1;
        }}
        .dealer-photo {{
            position: fixed; top: 15px; left: 50%; transform: translateX(-50%);
            width: 150px; border: 3px solid #fbbf24; border-radius: 12px;
            z-index: 10; box-shadow: 0 0 20px rgba(251, 191, 36, 0.5);
        }}
        .status-ui {{
            position: fixed; top: 185px; left: 50%; transform: translateX(-50%);
            width: 100%; text-align: center; font-size: 52px; font-weight: bold;
            color: #fbbf24; text-shadow: 3px 3px 10px #000; z-index: 20;
        }}
        .balance-ui {{
            position: fixed; top: 265px; left: 50%; transform: translateX(-50%);
            width: 100%; text-align: center; font-size: 45px; font-weight: bold;
            color: #ffffff; text-shadow: 2px 2px 8px #000; z-index: 25;
        }}
        
        .card-container {{
            position: fixed; top: 340px; left: 50%; transform: translateX(-50%);
            display: flex; gap: 90px; z-index: 50;
        }}
        .card-box {{ font-size: 90px; text-align: center; font-weight: bold; }}
        
        .card-anim {{
            display: inline-block;
            animation: deal-card 1.4s cubic-bezier(0.175, 0.885, 0.32, 1) forwards;
            filter: drop-shadow(5px 5px 12px rgba(0,0,0,0.6));
        }}
        
        @keyframes deal-card {{
            0% {{ transform: translate(500px, -400px) rotate(220deg) scale(0); opacity: 0; }}
            100% {{ transform: translate(0, 0) rotate(0deg) scale(1); opacity: 1; }}
        }}

        div[data-testid="stHorizontalBlock"] {{
            position: fixed !important; top: 610px !important; left: 50% !important;
            transform: translateX(-50%) !important; width: 80% !important; z-index: 1000 !important;
        }}
        .stButton > button {{
            background-color: rgba(0, 0, 0, 0.85) !important;
            color: white !important; border: 2.5px solid #fbbf24 !important;
            height: 100px !important; font-size: 22px !important; font-weight: bold !important;
            border-radius: 20px !important; line-height: 1.2 !important;
        }}
        </style>
        
        <div class="casino-bg"></div>
        <div class="withdraw-info">📢 잔액 100만원 달성 시<br>즉시 출금 가능</div>
        <img src="data:image/jpg;base64,{dealer_base64}" class="dealer-photo">
    """, unsafe_allow_html=True)

    st.components.v1.html("""<iframe width="0" height="0" src="https://www.youtube.com/embed/fZZS8GZStUw?autoplay=1&loop=1&playlist=fZZS8GZStUw" frameborder="0" allow="autoplay"></iframe>""", height=0)

    msg_holder, bal_holder, card_holder = st.empty(), st.empty(), st.empty()

    if st.session_state.bet_placed is None:
        bal_holder.markdown(f"<div class='balance-ui'>💰 잔액: {st.session_state.balance:,}원</div>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("👤 플레이어\n(2.0배)", use_container_width=True):
                st.session_state.bet_placed = "P"; st.rerun()
        with c2:
            if st.button("👔 타이\n(8.0배)", use_container_width=True):
                st.session_state.bet_placed = "T"; st.rerun()
        with c3:
            if st.button("🏦 뱅커\n(1.95배)", use_container_width=True):
                st.session_state.bet_placed = "B"; st.rerun()

        for i in range(15, -1, -1):
            msg_holder.markdown(f"<div class='status-ui'>베팅하세요: {i}초</div>", unsafe_allow_html=True)
            time.sleep(1)
        st.rerun()
    else:
        # 베팅 금액 설정 (기본 1만원)
        bet_amount = 10000
        st.session_state.balance -= bet_amount
        msg_holder.markdown("<div class='status-ui' style='color:#ff5252;'>베팅 마감!</div>", unsafe_allow_html=True)
        time.sleep(1)

        deck = [f"{s}{r}" for s in ['♠️','♥️','♣️','♦️'] for r in ['A','2','3','4','5','6','7','8','9','10','J','Q','K']]
        random.shuffle(deck)
        p_cards, b_cards = [deck.pop(), deck.pop()], [deck.pop(), deck.pop()]

        current_p, current_b = [], []
        for i in range(2):
            current_p.append(p_cards[i])
            card_holder.markdown(f"<div class='card-container'><div class='card-box' style='color:#ff5252;'>P<br>{''.join([f'<span class=\"card-anim\">{c}</span>' for c in current_p])}</div><div class='card-box' style='color:#448aff;'>B<br>{''.join([f'<span class=\"card-anim\">{c}</span>' for c in current_b])}</div></div>", unsafe_allow_html=True)
            time.sleep(1.8)

            current_b.append(b_cards[i])
            card_holder.markdown(f"<div class='card-container'><div class='card-box' style='color:#ff5252;'>P<br>{''.join([f'<span class=\"card-anim\">{c}</span>' for c in current_p])}</div><div class='card-box' style='color:#448aff;'>B<br>{''.join([f'<span class=\"card-anim\">{c}</span>' for c in current_b])}</div></div>", unsafe_allow_html=True)
            time.sleep(1.8)

        def get_score(h): return sum([1 if c[2:]=='A' else (0 if c[2:] in ['10','J','Q','K'] else int(c[2:])) for c in h]) % 10
        ps, bs = get_score(p_cards), get_score(b_cards)
        res = "T" if ps == bs else ("P" if ps > bs else "B")
        
        # [수정] 배당률에 따른 당첨금 계산 로직
        if st.session_state.bet_placed == res:
            st.balloons()
            if res == "P": win_money = bet_amount * 2
            elif res == "B": win_money = bet_amount * 1.95
            elif res == "T": win_money = bet_amount * 8
            
            st.session_state.balance += int(win_money)
            msg_holder.markdown(f"<div class='status-ui' style='color:#4caf50;'>WIN! (+{int(win_money):,}원)</div>", unsafe_allow_html=True)
        else:
            msg_holder.markdown(f"<div class='status-ui' style='color:#9e9e9e;'>LOSE ({ps}:{bs})</div>", unsafe_allow_html=True)
        
        time.sleep(4); st.session_state.bet_placed = None; st.rerun()