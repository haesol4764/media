import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# ==========================================
# 0. 페이지 기본 설정
# ==========================================
st.set_page_config(page_title="고령층 디지털 역량 강화 케어", layout="wide")

# 세션 상태 초기화 (페이지 간 데이터 공유용)
if 'scheduler' not in st.session_state:
    st.session_state.scheduler = None
if 'selected_apps' not in st.session_state:
    st.session_state.selected_apps = []

# 데이터 로드 함수
@st.cache_data
def load_data():
    return pd.read_csv("countries_media.csv")


# ==========================================
# 1. 각 페이지 화면을 함수로 정의 (경로 에러 원천 차단)
# ==========================================

def show_main_page():
    """ [1] 홈 & 데이터 대시보드 페이지 """
    st.title("👵👴 고령층 디지털 소외 해소를 위한 맞춤형 훈련 플랫폼")
    st.write("""
    본 플랫폼은 **'countries_media.csv'** 데이터를 기반으로, 만 60세 이상 시니어 계층의 디지털 기기 기능별 활용 현황을 분석하고, 
    어르신들이 디지털 세상에 쉽게 적응할 수 있도록 **개인 맞춤형 훈련 스케줄과 데일리 미션**을 제공합니다.
    """)
    st.markdown("---")
    
    try:
        df = load_data()
        st.subheader("📈 시니어 디지털 정보화 수준 분석 대시보드")
        
        years = df['시점'].unique()
        selected_year = st.selectbox("🎯 분석 년도 선택", years)
        filtered_df = df[df['시점'] == selected_year]
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"#### 👍 잘하시는 분야 ('그렇다' 비율이 높은 순)")
            yes_df = filtered_df[filtered_df['항목'].str.contains('그렇다')]
            top_5 = yes_df.sort_values(by='만60-69세', ascending=False).head(5)
            fig_top = px.bar(top_5, x='이용행태별(1)', y=['만60-69세', '만70세이상'],
                             barmode='group', title="상위 5개 디지털 역량 (%)")
            st.plotly_chart(fig_top, use_container_width=True)
            
        with col2:
            st.markdown(f"#### ⚠️ 도움이 필요한 분야 ('그렇지 않다' 비율이 높은 순)")
            no_df = filtered_df[filtered_df['항목'].str.contains('그렇지 않다')]
            bottom_5 = no_df.sort_values(by='만60-69세', ascending=False).head(5)
            fig_bottom = px.bar(bottom_5, x='이용행태별(1)', y=['만60-69세', '만70세이상'],
                                 barmode='group', title="하위 5개 디지털 역량 (어려움 체감 %)")
            st.plotly_chart(fig_bottom, use_container_width=True)
            
        st.markdown("### 📋 전체 데이터 분석 테이블")
        st.dataframe(filtered_df, use_container_width=True)
    except Exception as e:
        st.error(f"🚨 데이터를 불러오는 중 오류가 발생했습니다: {e}")


def show_training_page():
    """ [2] 개인별 맞춤 훈련 선택 페이지 """
    st.title("🎯 어르신 맞춤형 디지털 훈련 스케줄러")
    st.write("배우고 싶거나 평소에 어려웠던 스마트폰 기능을 선택하시면 맞춤형 학습 계획표를 만들어 드립니다.")

    app_options = {
        "💰 모바일 뱅킹 및 금융거래": ["계좌 이체하기", "은행 앱 로그인 및 보안카드 등록", "공과금 납부하기"],
        "🎫 쇼핑 및 예매/예약": ["쿠팡/기차표 예매하기", "병원 및 맛집 예약하기", "모바일 쿠폰 사용법"],
        "⚙️ 스마트폰 환경설정": ["Wi-Fi 및 블루투스 연결", "글자 크기 및 화면 밝기 조절", "벨소리 및 알림 설정"],
        "🔒 개인정보 및 피싱 예방": ["스팸/피싱 문자 구별하기", "비밀번호 안전하게 관리하기", "악성코드 검사하기"],
        "✉️ 이메일 및 서류 작성": ["이메일 열람 및 답장 쓰기", "스마트폰으로 간단한 메모/문서 작성"]
    }

    st.subheader("1. 배우고 싶은 스마트폰 기능을 골라주세요 (중복 선택 가능)")
    selected_categories = st.multiselect("학습 분야 선택", list(app_options.keys()), default=st.session_state.selected_apps)

    if selected_categories:
        st.subheader("2. 세부 학습 내용을 확인하세요")
        all_details = []
        for cat in selected_categories:
            with st.expander(f"🔍 {cat} 상세 커리큘럼"):
                for detail in app_options[cat]:
                    st.write(f"- {detail}")
                    all_details.append(detail)
        
        st.subheader("3. 훈련 강도 설정")
        intensity = st.radio("하루 훈련 횟수를 선택하세요", ["가볍게 (하루 1회)", "보통 (하루 2회)", "열정적으로 (하루 3회)"])
        
        if st.button("🗓️ 맞춤형 스케줄러 생성하기"):
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
            st.success("🎉 스케줄러가 완성되었습니다! '데일리 알림 & 실전 훈련' 메뉴에서 확인하세요.")

    if st.session_state.scheduler:
        st.markdown("---")
        st.subheader("📅 완성된 주간 계획표 요약")
        sched_df = pd.DataFrame(list(st.session_state.scheduler.items()), columns=["요일", "오늘의 훈련 목표"])
        st.table(sched_df)


def show_daily_page():
    """ [3] 데일리 알림 및 훈련 페이지 """
    st.title("📅 데일리 알림 및 실전 훈련")

    if not st.session_state.scheduler:
        st.warning("⚠️ 아직 맞춤형 스케줄러가 생성되지 않았습니다. '맞춤형 훈련 스케줄러' 메뉴에서 먼저 스케줄을 만들어주세요!")
        return

    st.subheader("⏰ 훈련 알림 시간 세팅")
    col1, col2 = st.columns(2)
    with col1:
        alert_time = st.time_input("알림을 받을 시간을 선택하세요", datetime.time(10, 0))
    with col2:
        use_sms = st.checkbox("문자 메시지(SMS)로도 알림 받기")
        
    if st.button("🔔 알림 설정 저장"):
        st.success(f"매일 {alert_time.strftime('%H시 %M분')}에 알림이 설정되었습니다.")

    st.markdown("---")
    st.subheader("🏃 오늘의 실전 미션 수행하기")
    days = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    weekday_idx = datetime.datetime.today().weekday()
    current_day = st.selectbox("오늘의 요일을 선택하세요", days, index=weekday_idx)
    
    todays_task = st.session_state.scheduler.get(current_day, "복습 및 자유 시간")
    st.info(f"### 📢 {current_day} 미션: **{todays_task}**")
    
    st.markdown("#### 🛠️ 미션 따라하기 가이드")
    if "금융" in todays_task or "이체" in todays_task:
        st.write("1. 스마트폰에서 은행 앱을 켭니다.\n2. '이체' 버튼을 누릅니다.\n3. 계좌번호를 천천히 입력해 봅니다.")
    elif "예매" in todays_task or "예약" in todays_task:
        st.write("1. '코레일톡' 또는 '쿠팡' 앱을 실행합니다.\n2. 목적지나 물건을 검색해 봅니다.")
    elif "설정" in todays_task or "네트워크" in todays_task:
        st.write("1. 스마트폰 '설정(톱니바퀴)'에 들어갑니다.\n2. 와이파이 상태나 글자 크기를 조절해 봅니다.")
    else:
        st.write("1. 배웠던 기능 중 어려웠던 점을 복습해 보세요.")

    st.markdown("---")
    if st.checkbox("🏆 오늘 미션을 성공적으로 마쳤습니다!"):
        st.balloons()
        st.success("훌륭합니다! 디지털 마스터에 한 걸음 더 가까워지셨습니다. 👍")


# ==========================================
# 2. 내비게이션 바 구성 및 앱 구동
# ==========================================
# 파일명 대신 위에서 선언한 함수명을 직접 인자로 연결합니다.
main_page = st.Page(show_main_page, title="홈 & 데이터 대시보드", icon="📊")
training_page = st.Page(show_training_page, title="맞춤형 훈련 스케줄러", icon="🎯")
daily_page = st.Page(show_daily_page, title="데일리 알림 & 실전 훈련", icon="📅")

pg = st.navigation([main_page, training_page, daily_page])
pg.run()
