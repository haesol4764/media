import streamlit as st

st.set_page_config(page_title="3단계: 주간 달력", layout="wide")

# 💡 세션 상태 유지 및 데이터 유실 방어선 고정
if 'selected_apps' not in st.session_state: st.session_state.selected_apps = []
if 'duration_weeks' not in st.session_state: st.session_state.duration_weeks = 2
if 'schedule_matrix' not in st.session_state: st.session_state.schedule_matrix = None
if 'completed_days' not in st.session_state: st.session_state.completed_days = set()

# 어르신 시인성 최적화 스타일링
st.markdown("""
    <style>
    html, body, [data-testid="stWidgetLabel"] p { font-size: 1.15rem !important; font-weight: bold !important; }
    h1 { font-size: 2.5rem !important; color: #1E3A8A; }
    h3 { font-size: 1.8rem !important; color: #1E40AF; margin-top: 20px !important; }
    </style>
""", unsafe_allow_html=True)

st.title("📅 나만의 한눈에 보는 가로 달력 계획표")
st.write("선택하신 기간 동안 단 하루도 똑같은 미션 없이, 매일 색다른 실생활 실습이 제공됩니다.")
st.markdown("---")

# 기능 카테고리별 알록달록 색상 배정 함수
def get_box_style(task_text, is_done):
    if is_done:
        return "background-color: #DCFCE7; border: 3px solid #22C55E; color: #15803D;"
    if "[병원]" in task_text or "[약국]" in task_text:
        return "background-color: #EFF6FF; border: 2px solid #3B82F6; color: #1E40AF;"
    elif "[금융]" in task_text:
        return "background-color: #FEF9C3; border: 2px solid #EAB308; color: #854D0E;"
    elif "[교통]" in task_text:
        return "background-color: #F5F3FF; border: 2px solid #8B5CF6; color: #5B21B6;"
    elif "[쇼핑]" in task_text or "[생활]" in task_text:
        return "background-color: #FFEDD5; border: 2px solid #F97316; color: #9A3412;"
    elif "[소통]" in task_text or "[여가]" in task_text:
        return "background-color: #FDF2F8; border: 2px solid #EC4899; color: #9D174D;"
    elif "[기본]" in task_text or "[보안]" in task_text:
        return "background-color: #F0FDF4; border: 2px solid #4ADE80; color: #166534;"
    else:
        return "background-color: #FAFAFA; border: 2px solid #737373; color: #404040;"

# 18대 기능별 100% 매일 다른 고유 미션 데이터베이스
DETAILED_MISSIONS = {
    "🏥 [병원] 병원 예약 및 똑닥 접수": ["[병원] 똑닥 어플을 홈 화면에서 찾아 가볍게 켜기", "[병원] 검색창에 우리동네 자주 가는 병원 이름 검색하기", "[병원] 의사 선생님 프로필 아래 [진료 접수] 버튼 확인하기", "[병원] 달력 화면에서 내가 원하는 날짜와 시간 골라보기", "[병원] 환자 정보가 맞는지 보고 최종 [예약 완료] 꾹 누르기"],
    "💊 [약국] 모바일 처방전 및 복약 알람": ["[약국] 처방전 종이에 인쇄된 사각형 [QR코드] 찾기", "[약국] 의료 앱을 열어 [모바일 처방전 등록] 버튼 누르기", "[약국] 카메라 사각형에 QR코드를 정확히 조준하기", "[약국] 스마트폰 기본 앱 중 [시계 -> 알람] 찾기", "[약국] 약 먹는 아침/저녁 시간에 맞춰 알람 만들고 저장하기"],
    "📜 [행정] 정부24 등본 발급 및 신분증": ["[행정] 스마트폰에서 [정부24] 앱 아이콘 가볍게 누르기", "[행정] 메인 화면 한가운데에 있는 [주민등록등본 발급] 누르기", "[행정] 인증 창에서 내 이름, 생년월일, 번호 천천히 치기", "[행정] 노란색 카카오톡 인증 요청을 누르고 비밀번호 입력하기", "[행정] 화면에 최종 발급된 등본 문서를 눈으로 확인하기"],
    "💰 [금융] 은행 앱(카카오뱅크/토스)으로 용돈 보내기": ["[금융] 내 스마트폰 전용 은행 앱을 누르고 로그인하기", "[금융] 내 계좌 잔액 바로 옆에 있는 큰 [이체] 글씨 누르기", "[금융] 돈을 보낼 가족이나 지인의 [은행 이름] 선택하기", "[금융] 보낼 [계좌번호]와 [금액]을 자판으로 천천히 입력하기", "[금융] 받는 사람 이름이 맞는지 확인 후 [비밀번호 6자리] 꾹 누르기"],
    "💳 [금융] 스마트폰으로 간편결제(삼성페이/카카오페이) 하기": ["[금융] 계산대 앞에서 스마트폰 화면 맨 아래를 위로 쓸어올리기", "[금융] 내 지문을 대거나 결제 비밀번호를 눌러 카드 활성화하기", "[금융] 사장님께 스마트폰 뒷면을 카드 단말기에 대달라고 요청하기", "[금융] 결제 완료 진동 소리와 함께 영수증 금액 확인하기"],
    "🎫 [교통] 기차표/고속버스 예매 (코레일톡/티머니)": ["[교통] 스마트폰에서 [코레일톡] 앱 아이콘 찾아서 누르기", "[교통] 내가 출발할 역과 도착할 역 이름을 각각 선택하기", "[교통] 기차를 탈 날짜와 대략적인 시간대를 달력에서 고르기", "[교통] 가운데에 있는 큰 [열차 조회하기] 파란 버튼 누르기", "[교통] 원하는 시간의 좌석을 누르고 카드번호를 입력해 예매하기"],
    "🚕 [교통] 카카오T로 집 앞까지 택시 호출하기": ["[교통] 스마트폰에서 노란색 바탕의 [카카오T] 앱 찾기", "[교통] 화면 위 자동차 모양의 [택시] 그림 톡 누르기", "[교통] [도착지 검색] 칸을 누르고 가고 싶은 목적지 이름 입력하기", "[교통] 화면을 올려 요금 중 가장 무난한 [일반 호출] 선택하기", "[교통] [기사님께 직접 결제] 옵션을 선택하고 큰 [호출하기] 누르기"],
    "🚇 [교통] 지하철/버스 도착 시간 확인하기 (카카오맵)": ["[교통] 내 스마트폰에서 [카카오맵 또는 지도 앱] 실행하기", "[교통] 상단 검색창에 지금 서 있는 버스 정류장 이름 검색하기", "[교통] 내가 타야 할 버스 번호나 지하철 방향 찾아 누르기", "[교통] 실시간으로 몇 분 뒤에 도착하는지 남은 시간 확인하기"],
    "🛒 [쇼핑] 쿠팡 장보기 및 무거운 쌀/물 배달시키기": ["[쇼핑] 로켓 모양의 [쿠팡] 앱 아이콘을 찾아 누르기", "[쇼핑] 맨 위 돋보기 모양 검색창을 손가락으로 가볍게 누르기", "[쇼핑] 자판으로 '생수' 또는 '화장지' 입력하고 검색하기", "[쇼핑] 수많은 물건 목록 중 마음에 드는 상품 그림 누르기", "[쇼핑] 아래 주황색 [구매하기]를 누르고 주문 끝내기"],
    "🍗 [쇼핑] 배달의민족으로 치킨/짜장면 시켜 먹기": ["[쇼핑] 민트색 [배달의민족] 앱을 찾아 누르기", "[쇼핑] 가운데 [배달]을 누르고 치킨이나 한식 카테고리 고르기", "[쇼핑] 평점이 좋은 식당을 하나 골라 메뉴판 구경하기", "[쇼핑] 먹고 싶은 음식 클릭 후 [장바구니에 담기] 누르기", "[쇼핑] 결제창에서 우리집 주소가 제대로 적혔는지 확인하기"],
    "🥕 [생활] 당근마켓으로 안 쓰는 물건 팔거나 나눔하기": ["[생활] 주황색 당근 모양의 [당근마켓] 앱 켜기", "[생활] 우측 하단 더하기 [+] 버튼을 누르고 [내 물건 팔기] 고르기", "[생활] 카메라 버튼을 누르고 팔거나 나눔할 물건 사진 찍기", "[생활] 글 제목과 나누고 싶은 가격(혹은 0원 나눔) 적기", "[생활] 오른쪽 위 [작성 완료] 버튼 눌러 동네에 글 올리기"],
    "📺 [여가] 유튜브 무료 검색 및 임영웅 노래 듣기": ["[여가] 빨간색 재생 버튼 모양의 [유튜브] 앱 켜기", "[여가] 오른쪽 맨 위 돋보기 모양 검색 아이콘 누르기", "[여가] 자판으로 '임영웅 최신 노래' 또는 ' 오늘의 뉴스' 치기", "[여가] 나오는 영상 중 마음에 드는 그림을 눌러 재생하기", "[여가] 영상 아래에 있는 빨간색 [구독] 글씨 꾹 눌러보기"],
    "📸 [소통] 카톡 단체방 사진 전송 및 보이스톡 걸기": ["[소통] 카카오톡을 켜고 자녀나 친구와의 대화방 들어가기", "[소통] 글자 입력칸 바로 왼쪽에 있는 더하기 [+] 버튼 누르기", "[소통] 초록색 산 모양의 [앨범] 아이콘 찾아 누르기", "[소통] 보낼 사진 동그라미를 선택하고 우측 상단 [전송] 누르기", "[소통] 수화기 모양 버튼을 누르고 무료 통화(보이스톡) 걸어보기"],
    "🎁 [소통] 카카오톡으로 생일 커피 쿠폰 선물하기": ["[소통] 카카오톡 친구 목록에서 이번 달 생일인 사람 찾기", "[소통] 프로필 화면 상단에 있는 상자 모양 [선물하기] 누르기", "[소통] 어르신들이 선물하기 좋은 커피나 빵 세트 고르기", "[소통] 노란색 [선물하기] 버튼을 누르고 결제 진행하기"],
    "⚙️ [기본] 와이파이 연결로 데이터 요금 아끼기": ["[기본] 스마트폰 맨 위 경계선에 대고 아래로 스윽 쓸어내리기", "[기본] 부채꼴 안테나 모양 [와이파이] 그림을 2초간 길게 누르기", "[기본] 내 주변 와이파이 이름 중 우리 집 이름 찾기", "[기본] 자판을 활용하여 비밀번호 대소문자 맞춰 천천히 입력하기"],
    "🔎 [기본] 글자 크기 돋보기처럼 아주 크게 키우기": ["[기본] 톱니바퀴 모양의 스마트폰 [설정] 앱 들어가기", "[기본] 화면을 조금 내려 [디스플레이 또는 화면] 누르기", "[기본] [글자 크기와 스타일] 메뉴를 찾아서 선택하기", "[기본] 맨 아래 조절 바의 파란 동그라미를 오른쪽 끝까지 밀기"],
    "🛡️ [보안] 스팸/피싱 문자 차단 및 절대 누르지 않기": ["[보안] 모르는 번호로 온 문자에 파란색 인터넷 링크 절대 안 누르기", "[보안] 문자 화면 오른쪽 위에 있는 [점 3개] 버튼 누르기", "[보안] [번호 차단] 또는 [스팸 신고] 문구를 찾아 차단하기", "[보안] 이미 확인한 광고 문자는 쓰레기통 버튼을 눌러 즉시 지우기"],
    "🤖 [실전] 식당/카페 무인 계산대(키오스크) 주문 결제": ["[실전] 식당이나 카페의 큰 주문 모니터 기계 앞에 서기", "[실전] 화면 아래 커다란 [주문하기] 또는 화면 자체를 터치하기", "[실전] 내가 먹고 싶은 음식 메뉴 그림을 손가락으로 꾹 누르기", "[실전] [포장하기]와 [매장 식사] 중 하나를 명확하게 고르기", "[실전] 카드 투입구 구멍 방향에 맞춰 신용카드 깊숙이 집어넣기"]
}

# 심화/응용 겹침 절대 방지용 7대 독립 행동 미션 풀
ADVANCED_VARIATIONS = [
    "어제 배웠던 유용한 단계를 자녀나 지인에게 직접 전화로 친절하게 설명해보기",
    "가이드북이나 도움 없이 오직 내 스마트폰 화면만 보고 똑같이 성공해보기",
    "오늘의 미션: 어제 배운 기능을 스마트폰을 완전히 껐다 켠 뒤 처음부터 켜보기",
    "나만의 배움 노트 미션: 오늘 배운 내용을 까먹지 않게 종이에 순서대로 적어보기",
    "스마트폰을 들고 동네 친구분을 만나 오늘 배운 멋진 기능을 직접 자랑하고 알려주기",
    "이번 주에 가장 어렵거나 헷갈렸던 단계를 골라 화면을 보며 5분간 천천히 복습하기",
    "오늘의 도전: 내가 배운 어플을 열고 평소 안 눌러보던 다른 메뉴도 살짝 터치해보기"
]

# 💡 [버그 제어 장치] 선택한 앱이 세션에 들어가 있다면, 스케줄 매트릭스가 비어있어도 여기서 실시간으로 강제 생성합니다.
if not st.session_state.selected_apps:
    st.warning("⚠️ 1단계 '학습 어플 및 기간 선택' 메뉴에서 배울 어플을 먼저 선택해 주세요!")
else:
    weeks = st.session_state.duration_weeks
    days_list = ["월", "화", "수", "목", "금", "토", "일"]
    
    # 선택된 앱 순서대로 고유 세부 미션들을 일렬로 수집
    dynamic_steps = []
    for app_key in st.session_state.selected_apps:
        if app_key in DETAILED_MISSIONS:
            dynamic_steps.extend(DETAILED_MISSIONS[app_key])
            
    # 매일 다른 미션들로 달력 캘린더 강제 구축 및 바인딩
    forced_schedule = {w: {d: "" for d in days_list} for w in range(1, weeks + 1)}
    step_idx = 0
    backup_idx = 0
    
    for w in range(1, weeks + 1):
        for d in days_list:
            if step_idx < len(dynamic_steps):
                forced_schedule[w][d] = dynamic_steps[step_idx]
                step_idx += 1
            else:
                # 정규 단계 소진 시, 선택한 카테고리 태그를 명시한 고유 심화 행동 부여
                if len(dynamic_steps) > 0:
                    base_task = dynamic_steps[backup_idx % len(dynamic_steps)]
                    app_hint = base_task.split(']')[0] + "]" if ']' in base_task else "[스마트폰]"
                else:
                    app_hint = "[스마트폰]"
                
                variation_text = ADVANCED_VARIATIONS[backup_idx % len(ADVANCED_VARIATIONS)]
                forced_schedule[w][d] = f"{app_hint} {variation_text}"
                backup_idx += 1
                
    st.session_state.schedule_matrix = forced_schedule

    # 상단 전체 진도율 바 계산
    total_slots = weeks * 7
    done_slots = len(st.session_state.completed_days)
    progress_percent = int((done_slots / total_slots) * 100)
    
    st.subheader(f"🏆 현재 어르신의 디지털 마스터 진도율: {progress_percent}% 완료")
    st.progress(done_slots / total_slots)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 가로 7칸 형태의 주차별 달력 생성 및 시각화
    for w in range(1, weeks + 1):
        st.markdown(f"### 🗓️ [ 제 {w} 주 차 ] 매일 다르게 배우는 달력")
        cols = st.columns(7)
        
        for idx, d in enumerate(days_list):
            with cols[idx]:
                task_text = st.session_state.schedule_matrix[w][d]
                is_done = (w, d) in st.session_state.completed_days
                
                badge = "✅ 완료" if is_done else "⏳ 오늘미션"
                box_design = get_box_style(task_text, is_done)
                
                st.markdown(f"""
                    <div style="{box_design} padding: 14px; border-radius: 12px; min-height: 190px; font-size: 1.0rem; box-shadow: 1px 2px 5px rgba(0,0,0,0.05);">
                        <center><span style="font-size: 1.1rem;"><b>{d}요일</b></span> <br> <small>({badge})</small></center>
                        <hr style='margin: 8px 0; border: 0.5px solid opacity 0.3;'>
                        <div style="line-height: 1.4;">{task_text}</div>
                    </div>
                """, unsafe_allow_html=True)
                
    st.markdown("---")
    st.info("💡 오늘 요일의 미션을 눈으로 확인하셨다면, 왼쪽 메뉴의 **'3 데일리 알림 및 실전 가이드'**로 이동하여 실제 스마트폰 훈련을 시작하세요!")
