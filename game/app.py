import streamlit as st
import random
import time

# 1. 페이지 설정 및 배경 고정
st.set_page_config(page_title="재국 라이브 스튜디오", page_icon="🎰", layout="wide")

# 2. 게임 상태 초기화
if 'balance' not in st.session_state: st.session_state.balance = 100000
if 'history' not in st.session_state: st.session_state.history = []
if 'game_started' not in st.session_state: st.session_state.game_started = False
if 'bet_placed' not in st.session_state: st.session_state.bet_placed = None
if 'bet_amount' not in st.session_state: st.session_state.bet_amount = 0

# 3. 레이아웃 고정 CSS (스크롤 방지 및 위치 고정)
st.markdown("""
    <style>
    /* 전체 화면 스크롤 금지 */
    html, body, [data-testid="stAppViewContainer"] {
        overflow: hidden;
        background-color: #000;
    }

    /* 빨간 테이블 (사이즈 대폭 확장 및 배경 고정) */
    .casino-table-main {
        position: fixed;
        top: 0; left: 0;
        width: 100%;
        height: 650px; /* 테이블 사이즈 늘림 */
        background: radial-gradient(circle, #b91d1d 0%, #2b0000 100%);
        border-bottom: 15px solid #3d2b1f;
        border-radius: 0 0 40% 40% / 0 0 10% 10%;
        z-index: 1;
    }

    /* 딜러 사진 (테이블 중앙 상단 고정) */
    .dealer-center {
        position: fixed;
        top: 40px;
        left: 50%;
        transform: translateX(-50%);
        width: 220px;
        border: 5px solid #fbbf24;
        border-radius: 15px;
        z-index: 10;
        box-shadow: 0 0 30px rgba(251, 191, 36, 0.4);
    }

    /* '베팅하세요' 글자 (중앙 고정 및 스크롤 불가) */
    .status-text-fixed {
        position: fixed;
        top: 280px;
        left: 50%;
        transform: translateX(-50%);
        width: 100%;
        text-align: center;
        font-size: 60px;
        font-weight: bold;
        color: #fbbf24;
        text-shadow: 0 0 20px rgba(0,0,0,0.8);
        z-index: 20;
    }

    /* 베팅 구역 (테이블 아래쪽 고정) */
    .betting-area-fixed {
        position: fixed;
        top: 670px; /* 테이블 끝나는 지점 아래 */
        width: 100%;
        padding: 20px;
        z-index: 30;
        background: #000;
    }

    /* 카드 날아오는 애니메이션 */
    .card-fly {
        font-size: 100px;
        display: inline-block;
        margin: 15px;
        animation: card-deal 1s cubic-bezier(0.25, 1, 0.5, 1) forwards;
    }
    @keyframes card-deal {
        0% { transform: translate(-400px, -200px) rotate(-180deg) scale(0); opacity: 0; }
        100% { transform: translate(0, 0) rotate(0deg) scale(1); opacity: 1; }
    }
    </style>
    """, unsafe_allow_html=True)

# 4. 음악 강제 재생 시스템 (유튜브 & 오디오 믹스)
st.components.v1.html("""
    <iframe width="0" height="0" src="https://www.youtube.com/embed/fZZS8GZStUw?autoplay=1&loop=1&playlist=fZZS8GZStUw&mute=0" 
    frameborder="0" allow="autoplay"></iframe>
    <audio id="bgm" loop><source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-15.mp3" type="audio/mpeg"></audio>
    <script>
        document.body.addEventListener('click', function() {
            var audio = document.getElementById('bgm');
            audio.play();
        }, {once: true});
    </script>
""", height=0)

# --- [인트로] ---
if not st.session_state.game_started:
    st.video("game/intro.mp4")
    if st.button("🧧 라이브 카지노 입장 (음악 활성화)", use_container_width=True):
        st.session_state.game_started = True
        st.rerun()

# --- [메인 게임] ---
else:
    # 테이블 배경과 딜러 사진 (HTML로 강제 고정)
    # 이미지 경로: 사진이 안나오는 문제를 위해 깃허브 절대 경로로 입력해주셔야 합니다. 
    # 아래 '본인의_깃허브_아이디' 부분을 실제 아이디로 바꿔주세요.
    st.markdown(f"""
        <div class="casino-table-main"></div>
        <img src="https://raw.githubusercontent.com/본인의_깃허브_아이디/본인의_레포지토리/main/game/dealer.jpg" class="dealer-center">
    """, unsafe_allow_html=True)

    msg_box = st.empty()
    card_box = st.empty()

    # 잔액 및 베팅 컨트롤 (테이블 아래쪽 하단)
    st.markdown(f"<div style='position:fixed; top:580px; width:100%; text-align:center; z-index:40;'>💰 현재 잔액: <span style='color:#fbbf24; font-size:30px;'>{st.session_state.balance:,}원</span></div>", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="betting-area-fixed">', unsafe_allow_html=True)
        if st.session_state.bet_placed is None:
            bet_amt = st.select_slider("베팅 칩 선택", options=[1000, 5000, 10000, 50000, 100000, 500000], value=10000)
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

            for i in range(15, -1, -1):
                msg_box.markdown(f"<div class='status-text-fixed'>베팅하세요: {i}초</div>", unsafe_allow_html=True)
                time.sleep(1)
            st.rerun()
        else:
            # 게임 진행 (베팅 종료)
            st.session_state.balance -= st.session_state.bet_amount
            msg_box.markdown("<div class='status-text-fixed' style='color:#f87171;'>베팅 마감!</div>", unsafe_allow_html=True)
            time.sleep(2)

            deck = [f"{s}{r}" for s in ['♠️','♥️','♣️','♦️'] for r in ['A','2','3','4','5','6','7','8','9','10','J','Q','K']]
            random.shuffle(deck)
            p_h, b_h = [deck.pop(), deck.pop()], [deck.pop(), deck.pop()]
            
            ps, bs = sum([1 if c[2:]=='A' else (0 if c[2:] in ['10','J','Q','K'] else int(c[2:])) for c in p_h]) % 10, \
                     sum([1 if c[2:]=='A' else (0 if c[2:] in ['10','J','Q','K'] else int(c[2:])) for c in b_h]) % 10

            msg_box.empty()
            p_v, b_v = [], []
            for i in range(2):
                p_v.append(p_h[i]); b_v.append(b_h[i])
                card_box.markdown(f"""
                    <div style='position:fixed; top:400px; left:50%; transform:translateX(-50%); display:flex; gap:100px; z-index:100;'>
                        <div class='card-fly' style='color:#f87171;'>P<br>{' '.join(p_v)}</div>
                        <div class='card-fly' style='color:#60a5fa;'>B<br>{' '.join(b_v)}</div>
                    </div>
                """, unsafe_allow_html=True)
                time.sleep(3.5)

            res = "T" if ps == bs else ("P" if ps > bs else "B")
            st.session_state.history.append(res)
            
            if (st.session_state.bet_placed == res): 
                mult = 9 if res=="T" else (2 if res=="P" else 1.95)
                win = int(st.session_state.bet_amount * mult)
                st.session_state.balance += win
                st.balloons()
                msg_box.markdown(f"<div class='status-text-fixed' style='color:#4ade80;'>🎉 {win:,}원 획득!</div>", unsafe_allow_html=True)
            else:
                msg_box.markdown("<div class='status-text-fixed' style='color:#9ca3af;'>낙첨되었습니다.</div>", unsafe_allow_html=True)
            
            time.sleep(4); st.session_state.bet_placed = None; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)