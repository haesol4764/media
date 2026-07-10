import streamlit as st

st.set_page_config(page_title="1단계: 조건 선택", layout="wide")

st.markdown("""
    <style>
    .stButton>button { font-size: 1.4rem !important; padding: 15px !important; background-color: #2563EB !important; color: white !important; width: 100%; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# 글로벌 세션 데이터 초기화
if 'selected_apps' not in st.session_state: st.session_state.selected_apps = []
if 'duration_weeks' not in st.session_state: st.session_state.duration_weeks = 2
if 'schedule_matrix' not in st.session_state: st.session_state.schedule_matrix = None
if 'completed_days' not in st.session_state: st.session_state.completed_days = set()

APP_CURRICULUM = {
    "💰 카카오뱅크로 돈 보내기 (금융)": [
        "스마트폰 화면에서 노란색 [카카오뱅크] 앱 버튼을 손가락으로 누르기",
        "내 계좌 옆에 있는 큰 [이체] 버튼 찾아서 누르기",
        "돈을 보낼 사람의 [은행 이름]을 목록에서 찾아 누르기",
        "보낼 [계좌번호]를 숫자 키패드로 천천히 한 글자씩 입력하기",
        "보낼 금액을 누르고, 아래 파란색 [다음] 버튼 누르기",
        "받는 사람 이름이 맞는지 확인하고, [비밀번호 6자리]를 꾹꾹 누르기"
    ],
    "🎫 기차표 예매하기 (코레일톡)": [
        "스마트폰에서 파란색 [코레일톡] 앱 아이콘 찾아서 누르기",
        "출발지와 목적지 버튼을 누르고 도시 선택하기",
        "출발하는 [날짜와 시간]을 달력 화면에서 손가락으로 가볍게 누르기",
        "가운데에 있는 큰 [열차 조회하기] 버튼 누르기",
        "원하는 시간대의 [순방향/일반실] 버튼을 찾아 누르기",
        "화면 아래의 [결제하기] 버튼을 누르고 카드번호 천천히 입력하기"
    ],
    "🛒 쿠팡으로 생활용품 장보기": [
        "스마트폰에서 로켓 모양 [쿠팡] 앱 아이콘을 찾아 누르기",
        "맨 위 돋보기 모양 [검색창]을 손가락으로 가볍게 톡 누르기",
        "자판으로 '화장지' 또는 '쌀'을 입력하고 자판의 [돋보기] 누르기",
        "물건 목록에서 맘에 드는 상품의 그림을 누르기",
        "화면 아래에 있는 주황색 [구매하기] 버튼 누르기",
        "주소가 맞는지 확인하고 [결제하기] 버튼을 아래로 밀거나 누르기"
    ],
    "⚙️ 와이파이(Wi-Fi) 주소 연결하기": [
        "스마트폰 맨 위 화면 가장자리를 손가락으로 대고 아래로 스윽 쓸어내리기",
        "부채꼴 모양의 [와이파이] 그림을 손가락으로 2초 동안 꾹~ 누르기",
        "와이파이 기능이 켜져 있는지 주황색/파란색 스위치 확인하기",
        "현재 있는 장소의 이름이 적힌 와이파이 글씨를 찾아 누르기",
        "알려준 [비밀번호]를 대소문자 구별해서 천천히 입력하기"
    ],
    "🛡️ 피싱/스팸 문자 차단 및 백신 검사": [
        "문자 메시지 앱을 켜고 모르는 번호로 온 의심스러운 문자 누르기",
        "문자 내용 안에 파란색 글씨로 적힌 인터넷 주소 절대 누르지 않기",
        "오른쪽 위 [점 3개] 버튼을 누르고 [번호 차단] 또는 [스팸 신고] 누르기",
        "스마트폰에 기본 설치된 [V3] 또는 [알약] 앱 아이콘 찾아서 누르기",
        "화면 한가운데에 있는 큰 [정밀 검사] 혹은 [최적화] 버튼 누르기"
    ]
}

st.title("🎯 배울 분야 및 목표 기간 정하기")
st.markdown("---")

st.subheader("🔵 1. 어떤 어플 기능을 배우고 싶으신가요? (여러 개 선택 가능)")
selected_apps = st.multiselect("원하는 기능을 선택하세요", list(APP_CURRICULUM.keys()), default=st.session_state.selected_apps)

st.subheader("🔵 2. 얼마 동안 나누어서 마스터하고 싶으신가요?")
duration_option = st.radio(
    "원하시는 학습 기간 버튼을 누르세요:",
    ["🏃 2주일 동안 빠르게 배우기", "🚶 3주일 동안 여유롭게 배우기", "🐢 한 달(4주일) 동안 완벽하게 마스터하기"]
)

weeks = 2 if "2주일" in duration_option else (3 if "3주일" in duration_option else 4)

if st.button("👉 이 큰 버튼을 누르시면 달력 스케줄표가 만들어집니다! 👈"):
    if not selected_apps:
        st.error("⚠️ 배우고 싶은 어플을 최소한 하나 이상 선택하셔야 합니다.")
    else:
        st.session_state.selected_apps = selected_apps
        st.session_state.duration_weeks = weeks
        
        days_list = ["월", "화", "수", "목", "금", "토", "일"]
        new_schedule = {w: {d: "" for d in days_list} for w in range(1, weeks + 1)}
        
        total_steps = []
        for app in selected_apps:
            for step in APP_CURRICULUM[app]:
                total_steps.append(f"{app.split()[1]} - {step}")
                
        step_idx = 0
        for w in range(1, weeks + 1):
            for d in days_list:
                if step_idx < len(total_steps):
                    new_schedule[w][d] = total_steps[step_idx]
                    step_idx += 1
                else:
                    if d in ["토", "일"]:
                        new_schedule[w][d] = "주말 실전 패밀리 미션: 자녀/손주에게 직접 시연하고 자랑하기"
                    else:
                        new_schedule[w][d] = "이전 단계 눈감고도 할 수 있도록 스마트폰 화면 다시 보며 복습하기"
                        
        st.session_state.schedule_matrix = new_schedule
        st.success("🎉 일정이 자동 생성되었습니다! '2_한눈에_보는_주간_달력' 메뉴로 이동해 주세요.")
