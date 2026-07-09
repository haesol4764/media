import streamlit as st
import pandas as pd

st.title("🎯 어르신 맞춤형 디지털 훈련 스케줄러")
st.write("배우고 싶거나 평소에 어려웠던 스마트폰 기능을 선택하시면 맞춤형 학습 계획표를 만들어 드립니다.")

# 세션 상태 초기화 (스케줄 저장용)
if 'scheduler' not in st.session_state:
    st.session_state.scheduler = None
if 'selected_apps' not in st.session_state:
    st.session_state.selected_apps = []

# 데이터셋의 주요 이용행태를 기반으로 카테고리 구성
app_options = {
    "💰 모바일 뱅킹 및 금융거래": ["계좌 이체하기", "은행 앱 로그인 및 보안카드 등록", "공과금 납부하기"],
    "🎫 쇼핑 및 예매/예약": ["쿠팡/기차표 예매하기", "병원 및 맛집 예약하기", "모바일 쿠폰 사용법"],
    "⚙️ 스마트폰 환경설정": ["Wi-Fi 및 블루투스 연결", "글자 크기 및 화면 밝기 조절", "벨소리 및 알림 설정"],
    "🔒 개인정보 및 피싱 예방": ["스팸/피싱 문자 구별하기", "비밀번호 안전하게 관리하기", "악성코드 검사하기"],
    "✉️ 이메일 및 서류 작성": ["이메일 열람 및 답장 쓰기", "스마트폰으로 간단한 메모/문서 작성"]
}

st.subheader("1. 배우고 싶은 스마트폰 기능을 골라주세요 (중복 선택 가능)")
selected_categories = st.multiselect("학습 분야 선택", list(app_options.keys()))

if selected_categories:
    st.subheader("2. 세부 학습 내용을 확인하세요")
    all_details = []
    for cat in selected_categories:
        with st.expander(f"🔍 {cat} 상세 커리큘럼"):
            for detail in app_options[cat]:
                st.write(f"- {detail}")
                all_details.append(detail)
    
    # 훈련 기간 및 강도 설정
    st.subheader("3. 훈련 강도 설정")
    intensity = st.radio("하루 훈련 횟수를 선택하세요", ["가볍게 (하루 1회)", "보통 (하루 2회)", "열정적으로 (하루 3회)"])
    
    if st.button("🗓️ 맞춤형 스케줄러 생성하기"):
        # 간이 주간 스케줄 매핑
        days = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
        schedule_data = {}
        
        detail_idx = 0
        for day in days:
            if detail_idx < len(all_details):
                schedule_data[day] = f"[{intensity.split()[0]}] {all_details[detail_idx]}"
                detail_idx += 1
            else:
                schedule_data[day] = "복습 및 자유 스마트폰 활용 시간"
                
        st.session_state.scheduler = schedule_data
        st.session_state.selected_apps = selected_categories
        st.success("🎉 어르신만의 맞춤형 7일 스케줄러가 완성되었습니다! '데일리 알림 & 실전 훈련' 페이지에서 확인하세요.")

# 생성된 스케줄러 미리보기
if st.session_state.scheduler:
    st.markdown("---")
    st.subheader("📅 완성된 주간 계획표 요약")
    sched_df = pd.DataFrame(list(st.session_state.scheduler.items()), columns=["요일", "오늘의 훈련 목표"])
    st.table(sched_df)
