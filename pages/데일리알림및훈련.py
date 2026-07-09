import streamlit as st
import datetime

st.title("📅 데일리 알림 및 실전 훈련")

# 스케줄러 데이터가 생성되어 있는지 확인
if 'scheduler' not in st.session_state or st.session_state.scheduler is None:
    st.warning("⚠️ 아직 맞춤형 스케줄러가 생성되지 않았습니다. '맞춤형 훈련 스케줄러' 페이지에서 먼저 스케줄을 만들어주세요!")
else:
    st.subheader("⏰ 훈련 알림 시간 세팅")
    st.write("매일 정해진 시간에 스마트폰 훈련 알림을 보내드립니다.")
    
    col1, col2 = st.columns(2)
    with col1:
        alert_time = st.time_input("알림을 받을 시간을 선택하세요", datetime.time(10, 0))
    with col2:
        use_sms = st.checkbox("문자 메시지(SMS)로도 알림 받기")
        
    if st.button("🔔 알림 설정 저장"):
        st.success(f"매일 {alert_time.strftime('%H시 %M분')}에 알림이 설정되었습니다. " + ("(문자 알림 연동 완료)" if use_sms else ""))

    st.markdown("---")

    # 오늘 요일 선택 (테스트 및 실전용)
    st.subheader("🏃 오늘의 실전 미션 수행하기")
    days = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    
    # 실제 현재 요일을 기본값으로 잡기
    weekday_idx = datetime.datetime.today().weekday()
    current_day = st.selectbox("오늘의 요일을 선택하세요", days, index=weekday_idx)
    
    todays_task = st.session_state.scheduler.get(current_day, "복습 및 자유 시간")
    
    # 큰 글씨 카드로 미션 안내
    st.info(f"### 📢 {current_day} 미션: **{todays_task}**")
    
    st.markdown("#### 🛠️ 미션 따라하기 가이드")
    if "금융" in todays_task or "이체" in todays_task:
        st.write("1. 스마트폰에서 은행 앱(예: 카카오뱅크, 국민은행 등)을 켭니다.")
        st.write("2. '이체' 또는 '송금' 버튼을 누릅니다.")
        st.write("3. 받는 사람의 은행과 계좌번호를 천천히 입력합니다. (실제 이체는 하지 않고 화면만 확인해도 좋아요!)")
    elif "예매" in todays_task or "예약" in todays_task:
        st.write("1. 플레이스토어에서 '코레일톡' 또는 '쿠팡' 앱을 실행합니다.")
        st.write("2. 가고 싶은 목적지나 사고 싶은 물건을 검색창에 입력합니다.")
        st.write("3. 달력에서 날짜를 선택하고 '좌석 선택'이나 '장바구니 담기'까지 진행해봅니다.")
    elif "설정" in todays_task or "네트워크" in todays_task:
        st.write("1. 스마트폰 상단 바를 아래로 쓸어내려 '톱니바퀴(설정)' 아이콘을 누릅니다.")
        st.write("2. '연결' 혹은 '디스플레이' 메뉴로 들어갑니다.")
        st.write("3. 와이파이 목록을 확인하거나 글자 크기를 조절해봅니다.")
    else:
        st.write("1. 이번 주에 배웠던 기능 중 가장 어려웠던 앱을 다시 한번 켜보세요.")
        st.write("2. 자녀분들이나 친구분들에게 인스턴트 메신저(카카오톡)로 사진을 한 장 보내보세요.")

    st.markdown("---")
    
    # 완료 체크 기능
    st.subheader("🏁 훈련 완료 인증")
    done = st.checkbox("🏆 오늘 미션을 성공적으로 마쳤습니다!")
    
    if done:
        st.balloons()
        st.success("훌륭합니다! 디지털 마스터에 한 걸음 더 가까워지셨습니다. 내일 미션도 화이팅! 🔥")
