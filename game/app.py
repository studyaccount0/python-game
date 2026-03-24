import streamlit as st
import random
import time

# 1. 페이지 설정
st.set_page_config(page_title="재국 라이브 카지노", page_icon="🎰", layout="wide")

# 2. 게임 상태 초기화
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'balance' not in st.session_state:
    st.session_state.balance = 100000
if 'history' not in st.session_state:
    st.session_state.history = []

# 3. 고급스러운 카지노 테이블 스타일 (CSS)
st.markdown("""
    <style>
    .main { background-color: #0d0d0d; color: white; }
    /* 테이블 디자인 */
    .casino-table { background: radial-gradient(circle, #800000 0%, #300000 100%); border-radius: 30px; padding: 40px; text-align: center; border: 10px solid #500; box-shadow: 0 0 30px rgba(0,0,0,0.8); position: relative; margin-bottom: 30px; }
    .dealer-img { border-radius: 50%; border: 5px solid #f1c40f; box-shadow: 0 0 15px rgba(241, 196, 15, 0.6); position: absolute; top: 20px; left: 50%; transform: translateX(-50%); width: 180px; height: 180px; object-fit: cover; }
    .card-area { background: rgba(0,0,0,0.2); border-radius: 15px; padding: 15px; text-align: center; border: 1px solid #444; }
    .card-display { font-size: 60px; display: inline-block; animation: flip 0.6s ease-in-out; margin: 10px; }
    @keyframes flip { from { transform: rotateY(90deg); opacity: 0; } to { transform: rotateY(0deg); opacity: 1; } }
    .score-circle { background: #f1c40f; color: black; border-radius: 50%; width: 50px; height: 50px; display: inline-flex; align-items: center; justify-content: center; font-weight: bold; font-size: 24px; margin-top: 15px; }
    
    /* 하단 베팅존 디자인 */
    .betting-zone { background-color: #222; border-radius: 20px; padding: 30px; text-align: center; margin-top: 20px; box-shadow: 0 -10px 20px rgba(0,0,0,0.5); }
    .history-dot { display: inline-block; width: 30px; height: 30px; border-radius: 50%; margin: 4px; text-align: center; font-size: 16px; font-weight: bold; line-height: 30px; color: white; box-shadow: 1px 1px 4px rgba(0,0,0,0.4); }
    .stButton>button { border-radius: 10px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- [인트로 화면] ---
if not st.session_state.game_started:
    st.video("game/intro.mp4")
    st.write("")
    if st.button("🎰 카지노 입장하기", use_container_width=True):
        st.session_state.game_started = True
        st.rerun()

# --- [메인 게임 화면] ---
else:
    # 카지노 테이블 영역
    st.markdown("<div class='casino-table'>", unsafe_allow_html=True)
    try:
        # game 폴더 내의 dealer.jpg 호출
        st.image("game/dealer.jpg")
    except:
        st.warning("dealer.jpg 파일을 'game' 폴더에 추가하면 딜러가 나타납니다.")
    
    st.markdown("<h2 style='color:#f1c40f; margin-top:200px;'>🎲 재국 라이브 카지노</h2>", unsafe_allow_html=True)
    
    # 스코어보드 (기록지)
    if st.session_state.history:
        h_html = "<div>"
        for res in st.session_state.history[-15:]:
            color = "#e74c3c" if res == "P" else ("#3498db" if res == "B" else "#2ecc71")
            h_html += f"<div class='history-dot' style='background:{color}'>{res}</div>"
        h_html += "</div>"
        st.markdown(h_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 잔액 표시
    st.markdown(f"<h3 style='text-align:right; color:white;'>💰 내 자산: {st.session_state.balance:,}원</h3>", unsafe_allow_html=True)
    
    st.write("---")

    # 카드 계산 로직
    def card_val(c):
        r = c.split()[1]
        if r in ['J', 'Q', 'K', '10']: return 0
        if r == 'A': return 1
        return int(r)

    # 카드 셔플 및 배분
    suits = ['♠️', '♥️', '♣️', '♦️']
    ranks = ranks = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
    deck = [f"{s} {r}" for s in suits for r in ranks]
    random.shuffle(deck)

    # 각 2장씩 배분
    p_hand = [deck.pop(), deck.pop()]
    b_hand = [deck.pop(), deck.pop()]
    p_score = (card_val(p_hand[0]) + card_val(p_hand[1])) % 10
    b_score = (card_val(b_hand[0]) + card_val(b_hand[1])) % 10

    # 바카라 3번째 카드 룰 적용
    if p_score <= 5 and b_score < 8:
        p_hand.append(deck.pop())
        p_score = sum(card_val(c) for c in p_hand) % 10
    
    if b_score <= 5 and p_score < 8:
        b_hand.append(deck.pop())
        b_score = sum(card_val(c) for c in b_hand) % 10

    # 승패 판정
    winner = ""
    if p_score > b_score: winner = "플레이어(2배)"
    elif b_score > p_score: winner = "뱅커(1.95배)"
    else: winner = "타이(9배)"

    # --- [하단 베팅존 영역] ---
    st.markdown("<div class='betting-zone'>", unsafe_allow_html=True)
    st.subheader("💳 베팅 영역")

    c_b1, c_b2, c_b3 = st.columns([1, 1, 1])
    with c_b1:
        bet_amount = st.number_input("베팅 금액 입력", min_value=1000, max_value=st.session_state.balance, step=5000, value=1000, label_visibility="collapsed")
    with c_b2:
        if st.button("💸 전액 베팅 (All-in)"):
            bet_amount = st.session_state.balance
            st.toast("🔥 가즈아! 올인 배팅 완료!", icon="🔥")
    with c_b3:
        pass # 여백

    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    with col_btn1:
        if st.button("👤 PLAYER (플레이어)", use_container_width=True):
            if st.session_state.balance < bet_amount: st.error("잔액이 부족합니다!")
            else:
                st.session_state.balance -= bet_amount
                progress_text = st.empty()
                for i in range(2, 0, -1):
                    progress_text.subheader(f"카드를 뒤집습니다... {i}")
                    time.sleep(0.5)
                progress_text.empty()
                
                res_p, res_b = st.columns(2)
                with res_p:
                    st.markdown("<div class='card-area'>", unsafe_allow_html=True)
                    st.subheader("👤 PLAYER")
                    for c in p_hand:
                        st.markdown(f"<span class='card-display'>{c}</span>", unsafe_allow_html=True)
                        time.sleep(0.4)
                    st.markdown(f"<br><div class='score-circle'>{p_score}</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with res_b:
                    st.markdown("<div class='card-area'>", unsafe_allow_html=True)
                    st.subheader("🏦 BANKER")
                    for c in b_hand:
                        st.markdown(f"<span class='card-display'>{c}</span>", unsafe_allow_html=True)
                        time.sleep(0.4)
                    st.markdown(f"<br><div class='score-circle'>{b_score}</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                if "플레이어" in winner:
                    mult = 2; st.session_state.history.append("P"); st.session_state.balance += int(bet_amount * mult); st.balloons(); st.success(f"🎊 당첨! {int(bet_amount * mult):,}원!")
                else:
                    if "타이" in winner: st.session_state.history.append("T"); st.info(f"결과는 타이입니다. {bet_amount:,}원이 반환됩니다."); st.session_state.balance += bet_amount
                    else: st.session_state.history.append("B"); st.error(f"낙첨되었습니다. 결과: {winner.split('(')[0]}")
                time.sleep(2); st.rerun()

    with col_btn2:
        if st.button("BANKER (뱅커)", use_container_width=True, type="primary"):
            if st.session_state.balance < bet_amount: st.error("잔액이 부족합니다!")
            else:
                st.session_state.balance -= bet_amount
                # 카드 오픈 애니메이션 등 PLAYER 버튼 로직과 동일 (생략)

    with col_btn3:
        if st.button("👔 TIE (타이)", use_container_width=True):
            if st.session_state.balance < bet_amount: st.error("잔액이 부족합니다!")
            else:
                st.session_state.balance -= bet_amount
                # 카드 오픈 애니메이션 등 PLAYER 버튼 로직과 동일 (생략)
    st.markdown("</div>", unsafe_allow_html=True)

    # 사이드바
    st.sidebar.button("💸 10만 원 즉시 충전", on_click=lambda: st.session_state.update(balance=100000))
    if st.sidebar.button("🏠 처음 화면으로"):
        st.session_state.game_started = False
        st.rerun()