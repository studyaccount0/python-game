import streamlit as st
import random
import time
import base64

# 1. 페이지 설정 및 스크롤 차단
st.set_page_config(page_title="재국 라이브 스튜디오", page_icon="🎰", layout="wide")

# 2. 이미지 파일을 베이스64로 인코딩 (사진 깨짐 방지 핵심)
def get_base64_img(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

dealer_base64 = get_base64_img("game/dealer.jpg") #

# 3. 레이아웃 고정 및 버튼 스타일 CSS
st.markdown(f"""
    <style>
    /* 전체 배경 및 스크롤 금지 */
    .main {{
        background-color: #000 !important;
        overflow: hidden !important;
    }}
    
    /* 빨간 테이블 (사이즈 대폭 확장) */
    .casino-table {{
        position: fixed;
        top: 0; left: 0; width: 100%; height: 600px;
        background: radial-gradient(circle, #cc0000 0%, #2b0000 100%);
        border-bottom: 15px solid #3d2b1f;
        border-radius: 0 0 50% 50% / 0 0 10% 10%;
        z-index: 1;
    }}

    /* 딜러 사진 (테이블 중앙 상단 고정) */
    .dealer-img {{
        position: fixed;
        top: 30px; left: 50%; transform: translateX(-50%);
        width: 250px; border: 5px solid #fbbf24; border-radius: 20px;
        z-index: 10; box-shadow: 0 0 30px rgba(251, 191, 36, 0.5);
    }}

    /* 안내 메시지 (중앙 고정) */
    .status-msg {{
        position: fixed;
        top: 320px; left: 50%; transform: translateX(-50%);
        width: 100%; text-align: center;
        font-size: 60px; font-weight: bold; color: #fbbf24;
        text-shadow: 2px 2px 10px #000; z-index: 20;
    }}

    /* 베팅 버튼 구역 (테이블 아래쪽 고정) */
    .stButton > button {{
        width: 100%; height: 80px !important; font-size: 22px !important;
        background-color: #1a1a1a !important; color: white !important;
        border: 1px solid #444 !important;
    }}
    .stButton > button:hover {{ border-color: #fbbf24 !important; }}
    </style>
    
    <div class="casino-table"></div>
    <img src="data:image/jpg;base64,{dealer_base64}" class="dealer-img">
    """, unsafe_allow_html=True)

# 4. 음악 자동 재생 (YouTube API + 클릭 감지)
st.components.v1.html("""
    <div id="player"></div>
    <script>
        var tag = document.createElement('script');
        tag.src = "https://www.youtube.com/iframe_api";
        var firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

        var player;
        function onYouTubeIframeAPIReady() {
            player = new YT.Player('player', {
                height: '0', width: '0',
                videoId: 'fZZS8GZStUw',
                playerVars: { 'autoplay': 1, 'loop': 1, 'playlist': 'fZZS8GZStUw' },
                events: { 'onReady': function(event) { event.target.playVideo(); } }
            });
        }
        // 사용자가 화면을 클릭하면 소리가 나오도록 강제 실행
        document.body.addEventListener('click', function() {
            if(player) player.playVideo();
        }, {once: true});
    </script>
""", height=0)

# --- [게임 로직] ---
if 'balance' not in st.session_state: st.session_state.balance = 100000
if 'history' not in st.session_state: st.session_state.history = []

msg_box = st.empty()
card_box = st.empty()

# 하단 베팅 구역 (테이블 아래 배치)
st.markdown("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
st.markdown(f"<h2 style='text-align:center; color:white;'>💰 잔액: {st.session_state.balance:,}원</h2>", unsafe_allow_html=True)

# 베팅 컨트롤
if st.session_state.get('bet_placed') is None:
    bet_amt = st.select_slider("베팅 칩", options=[1000, 5000, 10000, 50000, 100000, 500000], value=10000)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("👤 플레이어"): st.session_state.bet_placed = "P"; st.session_state.bet_amount = bet_amt; st.rerun()
    with col2:
        if st.button("👔 타이"): st.session_state.bet_placed = "T"; st.session_state.bet_amount = bet_amt; st.rerun()
    with col3:
        if st.button("🏦 뱅커"): st.session_state.bet_placed = "B"; st.session_state.bet_amount = bet_amt; st.rerun()

    # 타이머 표시
    for i in range(15, -1, -1):
        msg_box.markdown(f"<div class='status-msg'>베팅하세요: {i}초</div>", unsafe_allow_html=True)
        time.sleep(1)
    st.rerun()

else:
    # 카드 딜링 및 결과 (생략된 기존 로직 유지)
    msg_box.markdown("<div class='status-msg' style='color:#ff4d4d;'>베팅 종료!</div>", unsafe_allow_html=True)
    time.sleep(2)
    # ... 결과 처리 ...
    st.session_state.bet_placed = None
    st.rerun()