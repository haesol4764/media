import streamlit as st
import datetime

st.set_page_config(page_title="3단계: 알림 및 실전", layout="wide")

st.markdown("""
    <style>
    .guide-box { background-color: #F8FAFC; padding: 20px; border-left: 6px solid #2563EB; border-radius: 8px; margin-bottom: 15px; }
    .step-badge { background-color: #EF4444; color: white; padding: 3px 8px; border-radius: 5px; font-size: 1rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🏃 오늘의 알림 설정 및 단계적 실전 훈련")
st.markdown("---")

if 'schedule_matrix' not in st.session_state or not st.session_state.schedule_matrix:
    st.warning("⚠️ 먼저 앞 단계에서 스케줄러를 생성해야 실전 미션이 활성화됩니다.")
else:
    st.subheader("⏰ 1. 스마트폰 안 잊어버리게 알림 시간 맞추기")
    col1, col2 = st.columns(2)
    with col1:
        alert_time = st.time_input("훈련할 시간 선택:", datetime.time(10, 0))
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔔 이 시간을 알림 시계로 저장하기"):
            st.success(f"매일 {alert_time.strftime('%H시 %M분')}에 알림이 울립니다!")
            
    st.markdown("---")
    
    st.subheader("🎯 2. 오늘 내가 완수해야 할 훈련 단계")
    days_list = ["월", "화", "수", "목", "금", "토", "일"]
    
    w_select = st.selectbox("현재 배우고 계신 [주차]를 고르세요:", list(range(1, st.session_state.duration_weeks + 1)))
    d_select = st.selectbox("오늘의 [요일]을 고르세요:", days_list, index=datetime.datetime.today().weekday())
    
    current_task = st.session_state.schedule_matrix[w_select][d_select]
    st.warning(f"📢 미션 목표: {current_task}")
    
    # "큰 버튼을 누르고 꾹 누르세요" 가이드 출력 구성
    st.subheader("📱 3. 순서대로 따라 하기 가이드")
    
    # 기본 가이드 메시지 분할 출력
    steps = [
        "스마트폰 홈 화면에서 학습하려는 앱 아이콘을 눈으로 크~게 찾습니다.",
        "해당 앱을 손가락 끝으로 가볍게 톡 눌러서 실행시킵니다.",
        "화면에 나오는 글씨 중 '확인' 혹은 '다음'이라고 적힌 큰 파란색 버튼을 누릅니다.",
        "입력이 잘 안 될 때는 해당 빈칸 부분을 손가락으로 1초 동안 꾹~ 누른 후 다시 타이핑합니다."
    ]
    
    for idx, step_desc in enumerate(steps):
        st.markdown(f"""
            <div class="guide-box">
                <span class="step-badge">순서 {idx+1}</span> &nbsp;&nbsp; <b>{step_desc}</b>
            </div>
        """, unsafe_allow_html=True)
        
    st.info("💡 실전 실습을 완수하셨다면, '4_마무리_퀴즈_및_완료_도장' 메뉴로 가셔서 퀴즈를 풀고 도장을 받으세요!")
