import streamlit as st
import random
import time

# 1. 페이지 설정
st.set_page_config(page_title="재국 럭셔리 카지노", page_icon="🃏", layout="wide")

# 2. 게임 상태 초기화
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'balance' not in st.session_state:
    st.session_state.balance = 100000
if 'history' not in st.session_state:
    st.session_state.history = []

# 3. 고급스러운 카지노 스타일 (CSS)
st.markdown("""
    <style>
    .main { background-color: #013220; }
    .dealer-container { text-align: center; padding: 20px; }
    .dealer-img { border-radius: 50%; border: 4px solid #f1c40f; box-shadow: 0 0 15px rgba(241, 196, 15, 0.6); }
    .card-box { background: rgba(255,255,255,0.05); border-radius: 15px; padding: 20px; text-align: center; border: 1px solid #333; }
    .card-display { font-size: 55px; display: inline-block; animation: flip 0.6s ease-in-out; margin: 5px; }
    @keyframes flip { from { transform: rotateY(90deg); opacity: 0; } to { transform: rotateY(0deg); opacity: 1; } }
    .score-circle { background: #f1c40f; color: black; border-radius: 50%; width: 45px; height: 45px; display: inline-flex; align-items: center; justify-content: center; font-weight: bold; font-size: 22px; margin-top: 10px; }
    .history-dot { display: inline-block; width: 28px; height: 28px; border-radius: 50%; margin: 3px; text-align: center; font-size: 15px; font-weight: bold; line-height: 28px; color: white; box-shadow: 1px 1px 3px rgba(0,0,0,0.3); }
    </style>
    """, unsafe_allow_html=True)

# --- [인트로 화면] ---
if not st.session_state.game_started:
    st.video("intro.mp4")
    st.write("")
    if st.button("🎰 카지노 입장하기", use_container_width=True):
        st.session_state.game_started = True
        st.rerun()

# --- [메인 게임 화면] ---
else:
    # 딜러 이미지 노출 구역
    st.markdown("<div class='dealer-container'>", unsafe_allow_html=True)
    try:
        # game 폴더 내의 dealer.jpg 호출
        st.image("/Users/hvcfbbj/Desktop/python/game/dealer.jpg", width=220)
        st.markdown("<p style='color:#f1c40f; font-weight:bold;'>VVIP 전담 딜러</p>", unsafe_allow_html=True)
    except:
        st.warning("dealer.jpg 파일을 찾을 수 없습니다. 폴더 위치를 확인해주세요.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"<h2 style='text-align:center; color:white;'>💰 현재 잔액: {st.session_state.balance:,}원</h2>", unsafe_allow_html=True)
    
    # 스코어보드 (기록지)
    if st.session_state.history:
        st.write("📊 **최근 게임 로드맵**")
        h_html = "<div>"
        for res in st.session_state.history[-15:]:
            color = "#e74c3c" if res == "P" else ("#3498db" if res == "B" else "#2ecc71")
            h_html += f"<div class='history-dot' style='background:{color}'>{res}</div>"
        h_html += "</div>"
        st.markdown(h_html, unsafe_allow_html=True)

    st.write("---")

    # 베팅 설정
    col_set1, col_set2 = st.columns([2, 1])
    with col_set1:
        bet_target = st.radio("어디에 거시겠습니까?", ["플레이어(2배)", "뱅커(1.95배)", "타이(9배)"], horizontal=True)
    with col_set2:
        bet_amount = st.number_input("베팅 금액 입력", min_value=1000, max_value=st.session_state.balance, step=5000, value=1000)

    # 카드 계산 로직
    def card_val(c):
        r = c.split()[1]
        if r in ['J', 'Q', 'K', '10']: return 0
        if r == 'A': return 1
        return int(r)

    if st.button("🃏 CARDS OPEN", type="primary", use_container_width=True):
        st.session_state.balance -= bet_amount
        
        suits = ['♠️', '♥️', '♣️', '♦️']
        ranks = ranks = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
        deck = [f"{s} {r}" for s in suits for r in ranks]
        random.shuffle(deck)

        # 1단계: 각 2장씩 배분
        p_hand = [deck.pop(), deck.pop()]
        b_hand = [deck.pop(), deck.pop()]
        
        p_score = (card_val(p_hand[0]) + card_val(p_hand[1])) % 10
        b_score = (card_val(b_hand[0]) + card_val(b_hand[1])) % 10

        # 2단계: 바카라 3번째 카드 룰 적용
        # 플레이어 0~5일 때 한 장 더
        if p_score <= 5 and b_score < 8:
            p_hand.append(deck.pop())
            p_score = sum(card_val(c) for c in p_hand) % 10
        
        # 뱅커 0~5일 때 한 장 더 (간략화 룰)
        if b_score <= 5 and p_score < 8:
            b_hand.append(deck.pop())
            b_score = sum(card_val(c) for c in b_hand) % 10

        # 긴장감 넘치는 연출
        progress_text = st.empty()
        for i in range(3, 0, -1):
            progress_text.subheader(f"딜러가 카드를 오픈합니다... {i}")
            time.sleep(0.5)
        progress_text.empty()

        # 결과 화면 출력
        res_p, res_b = st.columns(2)
        with res_p:
            st.markdown("<div class='card-box'>", unsafe_allow_html=True)
            st.subheader("👤 PLAYER")
            for c in p_hand:
                st.markdown(f"<span class='card-display'>{c}</span>", unsafe_allow_html=True)
                time.sleep(0.5)
            st.markdown(f"<br><div class='score-circle'>{p_score}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with res_b:
            st.markdown("<div class='card-box'>", unsafe_allow_html=True)
            st.subheader("🏦 BANKER")
            for c in b_hand:
                st.markdown(f"<span class='card-display'>{c}</span>", unsafe_allow_html=True)
                time.sleep(0.5)
            st.markdown(f"<br><div class='score-circle'>{b_score}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # 승패 판정
        winner = ""
        if p_score > b_score: 
            winner = "플레이어(2배)"
            st.session_state.history.append("P")
        elif b_score > p_score: 
            winner = "뱅커(1.95배)"
            st.session_state.history.append("B")
        else: 
            winner = "타이(9배)"
            st.session_state.history.append("T")

        st.write("---")
        if bet_target == winner:
            rate = 2 if "플레이어" in winner else (1.95 if "뱅커" in winner else 9)
            win_total = int(bet_amount * rate)
            st.session_state.balance += win_total
            st.balloons()
            st.success(f"🎊 축하합니다! {win_total:,}원 당첨!")
        else:
            st.error(f"낙첨되었습니다. 결과: {winner.split('(')[0]}")

    # 사이드바
    st.sidebar.markdown(f"### 💳 현재 자산: {st.session_state.balance:,}원")
    if st.sidebar.button("💸 10만 원 즉시 충전"):
        st.session_state.balance = 100000
        st.rerun()
    if st.sidebar.button("🏠 처음 화면으로"):
        st.session_state.game_started = False
        st.rerun()