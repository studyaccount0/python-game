import streamlit as st
import random

# 사이트 설정 (제목, 아이콘)
st.set_page_config(page_title="나만의 커스텀 원카드", layout="wide")

st.title("🃏 AI와 함께하는 커스텀 원카드")
st.sidebar.header("⚙️ 게임 설정")

# 1. 난이도 조절 선택창
difficulty = st.sidebar.selectbox("AI 난이도를 선택하세요", ["쉬움", "보통", "어려움"])

# 2. 게임 상태 초기화 (데이터 저장용)
if 'player_hand' not in st.session_state:
    st.session_state.player_hand = ["카드1", "카드2", "카드3", "카드4", "카드5"]
    st.session_state.ai_hand_count = 5
    st.session_state.center_card = "스페이드 A"

# --- 화면 레이아웃 구성 ---

# 상단: AI 영역
st.subheader(f"🤖 AI 상대방 (난이도: {difficulty})")
cols_ai = st.columns(7)
for i in range(st.session_state.ai_hand_count):
    with cols_ai[i]:
        st.image("https://via.placeholder.com/100x150/FF0000/FFFFFF?text=Card", caption="AI 카드")

st.divider()

# 중앙: 버려진 카드 (현재 바닥에 놓인 카드)
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.write("📍 현재 바닥 카드")
    # 여기에 본인이 원하는 '바닥 카드' 이미지를 넣으세요
    st.image("https://via.placeholder.com/150x220/007bff/FFFFFF?text=Top+Card")

st.divider()

# 하단: 플레이어 영역 (내 카드)
st.subheader("👤 나의 카드 (클릭해서 내기)")
cols_player = st.columns(7)

for idx, card in enumerate(st.session_state.player_hand):
    with cols_player[idx]:
        # [중요] 여기에 본인이 원하는 사진 경로를 넣으면 됩니다!
        st.image("https://via.placeholder.com/100x150/000000/FFFFFF?text=My+Card", use_container_width=True)
        if st.button(f"{card} 내기", key=f"btn_{idx}"):
            st.success(f"{card}를 냈습니다!")
            # 실제 게임 로직(카드 삭제 등)이 들어갈 자리