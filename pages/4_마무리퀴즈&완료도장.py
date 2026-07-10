import streamlit as st
import datetime

st.set_page_config(page_title="4단계: 퀴즈 및 도장", layout="wide")

st.markdown("""
    <style>
    .stButton>button { font-size: 1.4rem !important; padding: 15px !important; background-color: #10B981 !important; color: white !important; width: 100%; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🏆 마무리 점검 퀴즈 및 도장 받기")
st.write("퀴즈와 미션 스크린샷 인증을 통과하면 배움 달력에 도장이 찍힙니다.")
st.markdown("---")

if 'schedule_matrix' not in st.session_state or not st.session_state.schedule_matrix:
    st.warning("⚠️ 이전 단계에서 미션을 진행한 후 이용해주세요.")
else:
    days_list = ["월", "화", "수", "목", "금", "토", "일"]
    col1, col2 = st.columns(2)
    with col1:
        w_tgt = st.selectbox("인증할 주차 고르기:", list(range(1, st.session_state.duration_weeks + 1)))
    with col2:
        d_tgt = st.selectbox("인증할 요일 고르기:", days_list, index=datetime.datetime.today().weekday())
        
    current_task = st.session_state.schedule_matrix[w_tgt][d_tgt]
    st.info(f"체크 대상 미션: {current_task}")
    
    st.markdown("### 📝 실전 마무리 안심 퀴즈")
    quiz_ans = st.radio(
        "Q. 스마트폰으로 거래나 예매 중 '모르는 사람'이 보낸 파란색 링크 주소를 눌러도 될까요?",
        ["1) 안전하니까 눌러서 확인해본다.", "2) 피싱 위험이 있으므로 절대로 누르지 않고 무시한다."]
    )
    
    st.markdown("### 📸 실제 스마트폰 화면 사진 인증하기")
    uploaded_file = st.file_uploader("스마트폰 캡처 사진 등록하기 (생략 가능)", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, caption="어르신이 등록하신 인증 화면", width=300)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🏆 최종 완료 도장 쾅 찍기! 🏆"):
        if "1)" in quiz_ans:
            st.error("❌ 퀴즈 틀렸습니다! 안전을 위해 모르는 주소는 절대로 누르면 안 됩니다. 정답을 다시 고르고 도장을 누르세요.")
        else:
            st.session_state.completed_days.add((w_tgt, d_tgt))
            st.balloons()
            st.success(f"👏 축하합니다! 제{w_tgt}주 {d_tgt}요일 달력 칸이 활성화되었습니다. '2_한눈에_보는_주간_달력'에서 연해진 초록색 칸을 확인하세요!")
