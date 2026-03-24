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

# 3. 사진 레이아웃 및 겹치기 CSS (핵심)
st.markdown("""
    <style>
    .main { background-color: #050505; color: white; }
    
    /* 1. 빨간 테이블 배경 (전체 상단 겹치기 기준) */
    .casino-background {
        background: radial-gradient(circle, #e63946 0%, #1b1b1b 100%);
        height: 500px;
        border-radius: 0 0 50% 50% / 0 0 15% 15%;
        border-bottom: 10px solid #5d4037;
        position: relative; /* 딜러와 글자를 겹치기 위한 기준점 */
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 0 20px 50px rgba(0,0,0,0.9);
        overflow: hidden;
    }

    /* 2. 딜러 이미지 (글자 위에 배치) */
    .dealer-wrap {
        position: absolute;
        top: 20px; /* 상단 고정 */
        z-index: 10;
        border: 4px solid #f1c40f;
        border-radius: 15px;
        box-shadow: 0 0 20px rgba(241, 196, 15, 0.5);
    }

    /* 3. 베팅 안내 글자 (딜러 밑에 배치) */
    .bet-status-text {
        margin-top: 180px; /* 딜러 사진 아래로 배치 */
        font-size: 55px;
        font-weight: bold;
        color: #f1c40f;
        text-shadow: 0 0 20px rgba(241, 196, 15, 0.8);
        z-index: 5;
    }

    /* 카드 애니메이션 */
    .card-fly {
        font-size: 80px; display: inline-block; margin: 10px;
        animation: card-deal 1.0s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
    }
    @keyframes card-deal {
        0% { transform: translateY(-300px) rotate(180deg) scale(0); opacity: 0; }
        100% { transform: translateY(0) rotate(0deg) scale(1); opacity: 1; }
    }

    /* 우측 하단 기록지 */
    .log-panel {
        position: fixed; bottom: 30px; right: 30px;
        background: rgba(0,0,0,0.9); padding: 15px; border-radius: 10px;
        border: 1px solid #444; display: grid; grid-template-columns: repeat(6, 25px); gap: 6px;
    }
    .dot { width: 22px; height: 22px; border-radius: 50%; font-size: 11px; text-align: center; line-height: 22px; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 4. 긴장감 넘치는 BGM (유튜브 배경음악 자동 재생)
st.markdown('<iframe src="https://www.youtube.com/embed/fZZS8GZStUw?autoplay=1&loop=1&playlist=fZZS8GZStUw" width="0" height="0" frameborder="0" allow="autoplay"></iframe>', unsafe_allow_html=True)

# --- [인트로 화면] ---
if not st.session_state.game_started:
    try:
        st.video("game/intro.mp4") #
    except:
        st.error("intro.mp4 파일을 확인해주세요.") #
    
    if st.button("🧧 라이브 카지노 입장하기", use_container_width=True):
        st.session_state.game_started = True
        st.rerun()

# --- [메인 스튜디오 화면] ---
else:
    # 1. 상단: 빨간 테이블 배경 + 딜러 + 안내 문구 (모두 겹치기)
    st.markdown("<div class='casino-background'>", unsafe_allow_html=True)
    
    # 딜러 이미지 (중앙 상단)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        try:
            st.markdown("<div class='dealer-wrap'>", unsafe_allow_html=True)
            st.image("game/dealer.jpg", width=200) #
            st.markdown("</div>", unsafe_allow_html=True)
        except:
            st.write("👤 [딜러 입장 대기 중]")
            
    # 안내 텍스트 및 카드 딜링 공간
    msg_placeholder = st.empty()
    card_placeholder = st.empty()
    st.markdown("</div>", unsafe_allow_html=True)

    # 2. 잔액 정보 (한국어)
    st.markdown(f"<h2 style='text-align:center;'>💰 현재 잔액: {st.session_state.balance:,}원</h2>", unsafe_allow_html=True)

    # 3. 베팅 로직 (15초)
    if st.session_state.bet_placed is None:
        st.write("---")
        # 칩 베팅 UI (한국어)
        bet_amt = st.select_slider("베팅할 칩 금액을 선택하세요", options=[1000, 5000, 10000, 50000, 100000, 500000], value=10000)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("👤 플레이어 (2.0x)", use_container_width=True):
                st.session_state.bet_placed = "P"; st.session_state.bet_amount = bet_amt; st.rerun()
        with c2:
            if st.button("👔 타이 (9.0x)", use_container_width=True):
                st.session_state.bet_placed = "T"; st.session_state.bet_amount = bet_amt; st.rerun()
        with c3:
            if st.button("🏦 뱅커 (1.95x)", use_container_width=True, type="primary"):
                st.session_state.bet_placed = "B"; st.session_state.bet_amount = bet_amt; st.rerun()

        # 15초 카운트다운 (딜러 사진 아래 위치)
        for i in range(15, -1, -1):
            msg_placeholder.markdown(f"<div class='bet-status-text' style='text-align:center;'>베팅하세요: {i}초</div>", unsafe_allow_html=True)
            time.sleep(1)
        st.rerun()

    else:
        # 베팅 완료 후 카드 공개 (15초 연출)
        st.session_state.balance -= st.session_state.bet_amount
        msg_placeholder.markdown("<div class='bet-status-text' style='text-align:center; color:#ff4d4d;'>베팅 종료 (NO MORE BETS)</div>", unsafe_allow_html=True)
        time.sleep(2)

        deck = [f"{s}{r}" for s in ['♠️','♥️','♣️','♦️'] for r in ['A','2','3','4','5','6','7','8','9','10','J','Q','K']]
        random.shuffle(deck)
        p_h, b_h = [deck.pop(), deck.pop()], [deck.pop(), deck.pop()]
        
        def score(h):
            s = sum([1 if c[2:]=='A' else (0 if c[2:] in ['10','J','Q','K'] else int(c[2:])) for c in h])
            return s % 10

        ps, bs = score(p_h), score(b_h)

        # 카드 한 장씩 천천히 공개 애니메이션
        msg_placeholder.empty()
        p_v, b_v = [], []
        for i in range(2):
            p_v.append(p_h[i])
            card_placeholder.markdown(f"""
                <div style='display:flex; justify-content:center; gap:100px; margin-top:200px;'>
                    <div class='card-fly' style='color:#e63946;'>플레이어<br>{' '.join(p_v)}</div>
                    <div class='card-fly' style='color:#3498db;'>뱅커<br>{' '.join(b_v)}</div>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(3.5)
            
            b_v.append(b_h[i])
            card_placeholder.markdown(f"""
                <div style='display:flex; justify-content:center; gap:100px; margin-top:200px;'>
                    <div class='card-fly' style='color:#e63946;'>플레이어<br>{' '.join(p_v)}</div>
                    <div class='card-fly' style='color:#3498db;'>뱅커<br>{' '.join(b_v)}</div>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(3.5)

        # 승패 판정 및 당첨금 표시
        res = "T" if ps == bs else ("P" if ps > bs else "B")
        st.session_state.history.append(res)
        
        win_money = 0
        if (st.session_state.bet_placed == "P" and res == "P"): win_money = st.session_state.bet_amount * 2
        elif (st.session_state.bet_placed == "B" and res == "B"): win_money = int(st.session_state.bet_amount * 1.95)
        elif (st.session_state.bet_placed == "T" and res == "T"): win_money = st.session_state.bet_amount * 9
        
        if win_money > 0:
            st.session_state.balance += win_money
            st.balloons()
            msg_placeholder.markdown(f"<div class='bet-status-text' style='text-align:center; color:#00ff00;'>🎊 축하합니다! {win_money:,}원 당첨!</div>", unsafe_allow_html=True)
        else:
            msg_placeholder.markdown(f"<div class='bet-status-text' style='text-align:center; color:#aaaaaa;'>아쉽게 낙첨되었습니다.</div>", unsafe_allow_html=True)
        
        time.sleep(4)
        st.session_state.bet_placed = None
        st.rerun()

    # 기록지 (로그)
    log_html = "<div class='log-panel'>"
    for r in st.session_state.history[-36:]:
        color = "#e63946" if r == "P" else ("#3498db" if r == "B" else "#00ff00")
        log_html += f"<div class='dot' style='background:{color}'>{r}</div>"
    log_html += "</div>"
    st.markdown(log_html, unsafe_allow_html=True)