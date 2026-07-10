import streamlit as st

st.set_page_config(page_title="데일리 가이드", layout="wide")

# 세션 상태 방어선 고정
if 'selected_apps' not in st.session_state: st.session_state.selected_apps = []
if 'duration_weeks' not in st.session_state: st.session_state.duration_weeks = 2
if 'schedule_matrix' not in st.session_state: st.session_state.schedule_matrix = None
if 'completed_days' not in st.session_state: st.session_state.completed_days = set()

# 어르신 전용 스타일 디자인
st.markdown("""
    <style>
    html, body, [data-testid="stWidgetLabel"] p { font-size: 1.15rem !important; font-weight: bold !important; }
    h1 { font-size: 2.3rem !important; color: #1E3A8A; }
    h3 { font-size: 1.6rem !important; color: #1E40AF; }
    .step-box { background-color: #F8FAFC; border-left: 5px solid #2563EB; padding: 15px; border-radius: 6px; margin-bottom: 12px; }
    .step-num { background-color: #EF4444; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold; margin-right: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("📱 오늘의 데일리 알림 및 실전 가이드")
st.markdown("---")

if st.session_state.schedule_matrix is None:
    st.warning("⚠️ 앞 단계에서 배우고 싶은 기능을 선택하고 스케줄표를 먼저 완성해 주세요!")
else:
    # 1. 주차 및 요일 셀렉터 배치
    weeks_list = list(range(1, st.session_state.duration_weeks + 1))
    days_list = ["월", "화", "수", "목", "금", "토", "일"]
    
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        selected_w = st.selectbox("📅 확인하고 싶은 [주차]를 고르세요:", weeks_list)
    with col_sel2:
        selected_d = st.selectbox("📆 오늘의 [요일]을 고르세요:", days_list)
        
    # 2. 오늘의 미션 텍스트 확정
    current_task = st.session_state.schedule_matrix[selected_w][selected_d]
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.info(f"📢 **제 {selected_w}주차 {selected_d}요일 미션 목표:**\n\n### {current_task}")
    st.markdown("---")
    
    st.subheader("📱 3. 순서대로 따라 하기 가이드")
    st.write("스마트폰을 손에 들고 아래 순서대로 천천히 따라 해보세요.")
    
    # 💡 [핵심 연동] 미션 문자열을 탐색하여 상황별 전용 4단계 가이드를 실시간 생성
    steps = []
    
    if "[병원]" in current_task:
        steps = [
            "스마트폰 홈 화면에서 파란색 똑닥 어플을 찾아 가볍게 터치하여 켭니다.",
            "맨 위 돋보기 모양 검색창을 누르고 우리 동네 다니시는 병원 이름을 천천히 입력합니다.",
            "의사 선생님 얼굴 아래에 있는 파란색 [진료 접수] 또는 [예약] 버튼을 누릅니다.",
            "달력이 뜨면 가고 싶으신 날짜와 시간을 손가락으로 콕 찍은 후 [완료]를 누릅니다."
        ]
    elif "[약국]" in current_task:
        steps = [
            "병원에서 받아온 종이 처방전 우측 상단에 있는 바코드나 사각형 QR코드를 찾습니다.",
            "스마트폰의 카메라 또는 전용 어플을 켜서 [모바일 처방전 등록] 기능을 실행합니다.",
            "네모난 카메라 화면 중앙에 처방전 QR코드가 쏙 들어오게 수평을 맞춰 대고 기다립니다.",
            "스마트폰의 [시계] 앱으로 들어가 약 먹는 시간에 맞춰 알람 소리를 새로 설정합니다."
        ]
    elif "[행정]" in current_task:
        steps = [
            "스마트폰에서 '정부24' 앱을 찾아서 누른 뒤, 메인 화면의 [주민등록등본 발급]을 선택합니다.",
            "내 이름과 주민등록번호를 자판으로 정확히 한 글자씩 입력합니다.",
            "화면에 카카오톡이나 패스 인증 요청이 오면 노란 버튼을 눌러 비밀번호를 찍어줍니다.",
            "인증이 끝나면 대기 화면이 지나가고 최종 완성된 문서가 화면에 나오는지 확인합니다."
        ]
    elif "[금융]" in current_task and "이체" in current_task:
        steps = [
            "은행 앱(카카오뱅크/토스 등)을 실행하고 지문이나 비밀번호로 안전하게 로그인합니다.",
            "내 계좌 잔액 바로 옆에 있는 커다란 [이체] 또는 [송금] 글씨를 찾아 누릅니다.",
            "돈을 보낼 가족의 은행 이름을 선택하고, 계좌번호와 보낼 금액 숫자를 천천히 입력합니다.",
            "받는 사람 이름(예: 아들, 딸)을 눈으로 다시 확인한 후 최종 송금 비밀번호를 입력합니다."
        ]
    elif "[금융]" in current_task and "결제" in current_task:
        steps = [
            "마트나 카페 계산대 앞에서 스마트폰 화면 맨 아래 테두리를 위로 쓸어 올립니다.",
            "화면에 신용카드가 나타나면 내 지문을 대거나 숫자 비밀번호를 눌러 불을 켭니다.",
            "가게 사장님께 스마트폰 뒷면을 카드 긁는 단말기 가까이에 대달라고 건네줍니다.",
            "띵동 하는 결제 완료 알림 진동 소리가 나면 금액이 맞는지 영수증을 체크합니다."
        ]
    elif "[교통]" in current_task and "기차표" in current_task:
        steps = [
            "스마트폰에서 코레일톡 어플을 찾아서 실행한 후 출발역과 도착역 이름을 각각 지정합니다.",
            "내가 가고자 하는 날짜와 대략적인 오전/오후 시간대를 달력에서 손가락으로 고릅니다.",
            "아래쪽 파란색 [열차 조회하기] 버튼을 눌러 예약 가능한 기차 시간 목록을 띄웁니다.",
            "원하는 시간대의 [선택] 버튼을 눌러 좌석을 지정하고 신용카드 번호로 예매를 마칩니다."
        ]
    elif "[교통]" in current_task and "택시" in current_task:
        steps = [
            "스마트폰에서 노란색 카카오T 어플을 켜고 상단 메뉴의 [택시] 그림을 가볍게 누릅니다.",
            "[어디로 갈까요?] 라고 적힌 빈 검색창에 가고 싶은 목적지 이름이나 건물을 입력합니다.",
            "추천 경로 요금 화면이 나오면 화면을 위로 올려 아래쪽에 숨겨진 [일반 호출]을 선택합니다.",
            "결제 수단 화면에서 [기사님께 직접 결제]를 선택한 후 하단 큰 [호출하기] 버튼을 누릅니다."
        ]
    elif "[쇼핑]" in current_task:
        steps = [
            "쿠팡이나 배달 앱 아이콘을 찾아 누르고, 맨 위 돋보기 모양 검색 영역을 톡 누릅니다.",
            "내가 오늘 사거나 먹고 싶은 물건(예: 생수, 치킨)의 이름을 입력하고 검색을 누릅니다.",
            "목록에 나오는 물건들의 그림과 가격을 천천히 구경한 후 마음에 드는 상품을 선택합니다.",
            "하단의 주황색 또는 빨간색 [구매하기]나 [장바구니 담기] 버튼을 눌러 주문을 진행합니다."
        ]
    elif "[여가]" in current_task or "유튜브" in current_task:
        steps = [
            "홈 화면에서 빨간색 재생 버튼 모양의 [유튜브] 앱을 찾아 가볍게 터치합니다.",
            "우측 상단 모서리에 있는 작은 돋보기 모양(검색 아이콘)을 찾아 손가락으로 누릅니다.",
            "자판을 이용하여 '임영웅 노래' 혹은 '뉴스'라고 글씨를 치고 돋보기 자판을 누릅니다.",
            "노래 영상 목록이 나타나면 보고 싶은 영상의 사진 부분을 터치하여 노래를 감상합니다."
        ]
    elif "[소통]" in current_task:
        steps = [
            "카카오톡을 실행하여 대화 목록에서 소통하고 싶은 자녀나 친구의 이름을 찾아 방에 들어갑니다.",
            "글자 쓰는 칸 바로 왼쪽에 숨겨진 더하기 모양 [+] 아이콘 버튼을 가볍게 툭 누릅니다.",
            "메뉴가 열리면 초록색 산 모양의 [앨범]을 누르고 전송할 사진 동그라미를 선택합니다.",
            "오른쪽 맨 위에 있는 [전송] 글씨를 누르거나, 수화기 그림을 눌러 무료 통화를 시작합니다."
        ]
    elif "[기본]" in current_task or "[보안]" in current_task:
        steps = [
            "스마트폰 화면의 맨 위 경계선에 손가락을 대고 커튼을 치듯 아래로 스윽 쓸어내립니다.",
            "톱니바퀴 모양의 [설정] 아이콘을 누르고 [디스플레이] 또는 [보안/차단] 메뉴로 진입합니다.",
            "글자 크기 조절 바를 오른쪽으로 밀어 크게 키우거나 모르는 스팸 번호를 찾아 누릅니다.",
            "변경 사항이 정상적으로 반영되었는지 확인한 후 홈 버튼을 눌러 첫 화면으로 빠져나옵니다."
        ]
    else:
        # 💡 응용/복습 미션일 때 각 상황에 맞춰 유연하게 변환되는 가이드
        steps = [
            "달력에 표시된 오늘의 응용 과제 내용을 마음속으로 소리 내어 한 번 읽어봅니다.",
            "오늘 미션에 적힌 어플이나 스마트폰 기능을 켜기 위해 홈 화면으로 이동합니다.",
            "보조 가이드북이나 가족들의 도움을 받지 않고 오직 내 기억과 손 끝 감각만으로 앱을 다뤄봅니다.",
            "실습이 끝났다면 오늘 새롭게 알게 된 점이나 헷갈렸던 메뉴를 공책에 나만의 메모로 남겨둡니다."
        ]
        
    # 완성된 4단계 동적 가이드를 큰 글씨 박스로 화면에 출력
    for i, step_text in enumerate(steps, 1):
        st.markdown(f"""
            <div class="step-box">
                <span class="step-num">순서 {i}</span>
                <span style="font-size: 1.15rem; color: #334155;">{step_text}</span>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.success("💡 실전 실습을 완료하셨다면, 왼쪽 메뉴의 **'4 마무리 퀴즈 및 완료 도장'**으로 가셔서 문제를 풀고 도장을 꾹 받아 가세요!")
