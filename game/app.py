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

# 3. 레이어 통합 CSS (배경 위에 사진과 글자를 강제로 올림)
st.markdown("""
    <style>
    .main { background-color: #000; }
    
    /* 전체 스튜디오 컨테이너 */
    .studio-layer {
        position: relative;
        width: 100%;
        height: 550px;
        background: radial-gradient(circle, #e63946 0%, #2b0000 100%);
        border-radius: 0 0 50% 50% / 0 0 15% 15%;
        border-bottom: 10px solid #4e342e;
        overflow: hidden;
        display: flex;
        justify-content: center;
        box-shadow: 0 20px 50px rgba(0,0,0,0.9);
    }

    /* 딜러 사진: 배경 위에 절대 위치로 고정 */
    .dealer-on-table {
        position: absolute;
        top: 20px;
        width: 220px;
        border: 4px solid #ffca28;
        border-radius: 15px;
        z-index: 10; /* 배경보다 위 */
        box-shadow: 0 0 30px rgba(255, 202, 40, 0.5);
    }

    /* 상태 메시지: 딜러 사진보다 더 위에 배치 */
    .text-overlay {
        position: absolute;
        top: 250px;
        width: 100%;
        text-align: center;
        font-size: 55px;
        font-weight: bold;
        color: #ffca28;
        text-shadow: 0 0 20px rgba(0,0,0,1);
        z-index: 20; /* 딜러 사진보다 위 */
    }

    /* 카드 애니메이션: 슈(Shoe)에서 날아오는 효과 */
    .card-fly {
        font-size: 90px;
        display: inline-block;
        margin: 15px;
        filter: drop-shadow(5px 5px 10px rgba(0,0,0,0.5));
        animation: deal-effect 1.1s cubic-bezier(0.25, 1, 0.5, 1) forwards;
    }
    @keyframes deal-effect {
        0% { transform: translate(-400px, -200px) rotate(-180deg) scale(0); opacity: 0; }
        100% { transform: translate(0, 0) rotate(0deg) scale(1); opacity: 1; }
    }
    </style>
    """, unsafe_allow_html=True)

# 4. 사운드 시스템 (강제 자동 재생 코드)
# 팁: 브라우저가 소리를 막을 수 있으니, 입장 버튼을 꼭 눌러주세요!
st.components.v1.html("""
    <script>
        function playAudio() {
            var audio = new Audio('https://www.soundhelix.com/examples/mp3/SoundHelix-Song-15.mp3');
            audio.loop = true;
            audio.play();
        }
    </script>
    <iframe width="0" height="0" src="https://www.youtube.com/embed/fZZS8GZStUw?autoplay=1&loop=1&playlist=fZZS8GZStUw" frameborder="0" allow="autoplay"></iframe>
""", height=0)

# --- [게임 시작 전 인트로] ---
if not st.session_state.game_started:
    st.video("game/intro.mp4")
    if st.button("🧧 라이브 스튜디오 입장 (소리 재생)", use_container_width=True):
        st.session_state.game_started = True
        st.rerun()

# --- [메인 게임 화면] ---
else:
    # 1. 상단 스튜디오 (HTML로 레이어 강제 통합)
    st.markdown(f"""
        <div class="studio-layer">
            <img src="https://raw.githubusercontent.com/재국님레포/main/game/dealer.jpg" class="dealer-on-table">
            <div class="text-overlay" id="status-text"></div>
        </div>
    """, unsafe_allow_html=True)
    
    # 겹쳐진 레이어 위에 글자와 카드를 띄우기 위한 placeholder
    msg_box = st.empty()
    card_box = st.empty()

    # 2. 잔액 표시
    st.markdown(f"<h1 style='text-align:center; color:white;'>💰 현재 잔액: {st.session_state.balance:,}원</h1>", unsafe_allow_html=True)

    # 3. 게임 엔진
    if st.session_state.bet_placed is None:
        st.write("---")
        bet_amt = st.select_slider("베팅 금액을 선택하세요", options=[1000, 5000, 10000, 50000, 100000, 500000], value=10000)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("플레이어 (2.0x)", use_container_width=True):
                st.session_state.bet_placed = "P"; st.session_state.bet_amount = bet_amt; st.rerun()
        with c2:
            if st.button("타이 (9.0x)", use_container_width=True):
                st.session_state.bet_placed = "T"; st.session_state.bet_amount = bet_amt; st.rerun()
        with c3:
            if st.button("뱅커 (1.95x)", use_container_width=True, type="primary"):
                st.session_state.bet_placed = "B"; st.session_state.bet_amount = bet_amt; st.rerun()

        # 15초 베팅 타이머 (딜러 사진 위에 겹쳐서 표시)
        for i in range(15, -1, -1):
            msg_box.markdown(f"""<div style='position:fixed; top:350px; left:50%; transform:translateX(-50%); font-size:55px; font-weight:bold; color:#ffca28; z-index:100;'>베팅하세요: {i}초</div>""", unsafe_allow_html=True)
            time.sleep(1)
        st.rerun()

    else:
        # 베팅 완료 후 카드 공개 (15초 소요)
        st.session_state.balance -= st.session_state.bet_amount
        msg_box.markdown(f"""<div style='position:fixed; top:350px; left:50%; transform:translateX(-50%); font-size:55px; font-weight:bold; color:#ff4d4d; z-index:100;'>베팅 마감!</div>""", unsafe_allow_html=True)
        time.sleep(2)

        deck = [f"{s}{r}" for s in ['♠️','♥️','♣️','♦️'] for r in ['A','2','3','4','5','6','7','8','9','10','J','Q','K']]
        random.shuffle(deck)
        p_h, b_h = [deck.pop(), deck.pop()], [deck.pop(), deck.pop()]
        
        def score(h):
            s = sum([1 if c[2:]=='A' else (0 if c[2:] in ['10','J','Q','K'] else int(c[2:])) for c in h])
            return s % 10

        ps, bs = score(p_h), score(b_h)

        # 카드 딜링 애니메이션 (한 장씩 3.5초 간격)
        msg_box.empty()
        p_v, b_v = [], []
        for i in range(2):
            p_v.append(p_h[i])
            card_box.markdown(f"""
                <div style='position:fixed; top:420px; left:50%; transform:translateX(-50%); display:flex; gap:100px; z-index:100;'>
                    <div class='card-fly' style='color:#e63946;'>P<br>{' '.join(p_v)}</div>
                    <div class='card-fly' style='color:#3498db;'>B<br>{' '.join(b_v)}</div>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(3.5)
            
            b_v.append(b_h[i])
            card_box.markdown(f"""
                <div style='position:fixed; top:420px; left:50%; transform:translateX(-50%); display:flex; gap:100px; z-index:100;'>
                    <div class='card-fly' style='color:#e63946;'>P<br>{' '.join(p_v)}</div>
                    <div class='card-fly' style='color:#3498db;'>B<br>{' '.join(b_v)}</div>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(3.5)

        # 결과 및 당첨 처리
        res = "T" if ps == bs else ("P" if ps > bs else "B")
        st.session_state.history.append(res)
        
        win_money = 0
        if (st.session_state.bet_placed == "P" and res == "P"): win_money = st.session_state.bet_amount * 2
        elif (st.session_state.bet_placed == "B" and res == "B"): win_money = int(st.session_state.bet_amount * 1.95)
        elif (st.session_state.bet_placed == "T" and res == "T"): win_money = st.session_state.bet_amount * 9
        
        if win_money > 0:
            st.session_state.balance += win_money
            st.balloons()
            msg_box.markdown(f"<div style='position:fixed; top:350px; left:50%; transform:translateX(-50%); font-size:55px; font-weight:bold; color:#00ff00; z-index:100;'>🎉 {win_money:,}원 당첨! (총액: {st.session_state.balance:,}원)</div>", unsafe_allow_html=True)
        else:
            msg_box.markdown(f"<div style='position:fixed; top:350px; left:50%; transform:translateX(-50%); font-size:55px; font-weight:bold; color:#aaaaaa; z-index:100;'>낙첨되었습니다.</div>", unsafe_allow_html=True)
        
        time.sleep(4)
        st.session_state.bet_placed = None
        st.rerun()

    # 기록지
    log_html = "<div style='position:fixed; bottom:20px; right:20px; display:grid; grid-template-columns:repeat(6,25px); gap:5px; background:rgba(0,0,0,0.8); padding:10px; border-radius:10px;'>"
    for r in st.session_state.history[-36:]:
        c = "#e63946" if r == "P" else ("#3498db" if r == "B" else "#00ff00")
        log_html += f"<div style='width:22px; height:22px; background:{c}; border-radius:50%; color:white; font-size:11px; text-align:center; line-height:22px; font-weight:bold;'>{r}</div>"
    log_html += "</div>"
    st.markdown(log_html, unsafe_allow_html=True)