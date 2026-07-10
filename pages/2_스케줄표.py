import streamlit as st

st.set_page_config(page_title="1단계: 조건 선택", layout="wide")

st.markdown("""
    <style>
    html, body, [data-testid="stWidgetLabel"] p { font-size: 1.15rem !important; font-weight: bold !important; }
    .stButton>button { font-size: 1.4rem !important; padding: 15px !important; background-color: #2563EB !important; color: white !important; width: 100%; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# 세션 상태 유지 방어선
if 'selected_apps' not in st.session_state: st.session_state.selected_apps = []
if 'duration_weeks' not in st.session_state: st.session_state.duration_weeks = 2
if 'schedule_matrix' not in st.session_state: st.session_state.schedule_matrix = None
if 'completed_days' not in st.session_state: st.session_state.completed_days = set()

# 18대 세분화 커리큘럼 데이터셋
APP_CURRICULUM = {
    "🏥 [병원] 병원 예약 및 똑닥 접수": ["[똑닥 어플]을 화면에서 찾아 켜기", "[돋보기창]에 우리동네 병원 이름 검색하기", "의사 선생님 프로필 아래 [진료 접수/예약] 누르기", "달력에서 원하는 [날짜와 시간] 손가락으로 고르기", "내 정보가 맞는지 보고 [예약 완료] 꾹 누르기"],
    "💊 [약국] 모바일 처방전 및 복약 알람": ["병원 처방전 종이의 [QR코드] 찾기", "의료 앱에서 [모바일 처방전 등록] 버튼 누르기", "카메라 화면 사각형에 QR코드 조준하기", "스마트폰 [시계 -> 알람] 메뉴 들어가기", "약 먹는 시간에 맞춰 알람 새로 만들고 [저장] 누르기"],
    "📜 [행정] 정부24 등본 발급 및 신분증": ["[정부24] 앱 아이콘 가볍게 누르기", "메인 화면 가운데 [주민등록등본 발급] 누르기", "인증 창에서 내 [이름, 생년월일, 번호] 치기", "노란색 카카오톡 인증 요청 누르고 비밀번호 입력하기", "화면에 뜬 등본 문서를 눈으로 확인하기"],
    "💰 [금융] 은행 앱(카카오뱅크/토스)으로 용돈 보내기": ["[카카오뱅크] 앱을 누르고 로그인하기", "내 계좌 잔액 옆 큰 [이체] 글씨 누르기", "돈 보낼 사람의 [은행 이름] 고르기", "보낼 [계좌번호]와 [보낼 금액] 숫자로 치기", "받는 사람 이름 재확인 후 [비밀번호 6자리] 누르기"],
    "💳 [금융] 스마트폰으로 간편결제(삼성페이/카카오페이) 하기": ["스마트폰 켜진 상태에서 화면 맨 아래를 위로 쓸어올리기", "지문 인식이나 결제 비밀번호 눌러 카드 띄우기", "카드 단말기 근처에 스마트폰 뒷면 대기", "결제 완료 진동과 금액 확인하기"],
    "🎫 [교통] 기차표/고속버스 예매 (코레일톡/티머니)": ["[코레일톡] 앱 아이콘 찾아서 누르기", "출발지와 목적지(역 이름) 각각 선택하기", "기차 타고 갈 [날짜와 시간] 달력에서 고르기", "중앙의 [열차 조회하기] 파란 버튼 누르기", "원하는 시간의 [일반실 좌석] 선택 후 결제하기"],
    "🚕 [교통] 카카오T로 집 앞까지 택시 호출하기": ["[카카오T] 앱을 찾아 누르기", "자동차 모양 [택시] 그림 톡 누르기", "[도착지 검색] 칸에 가고 싶은 목적지 입력하기", "여러 요금 중 [일반 호출] 누르기", "[기사님께 직접 결제] 선택 후 아래 큰 [호출하기] 누르기"],
    "🚇 [교통] 지하철/버스 도착 시간 확인하기 (카카오맵)": ["[카카오맵 또는 지도 앱] 켜기", "상단 검색창에 지금 서 있는 정류장/역 이름 치기", "내가 탈 버스 번호나 지하철 방향
