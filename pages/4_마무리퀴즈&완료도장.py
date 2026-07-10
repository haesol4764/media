import streamlit as st

st.set_page_config(page_title="마무리 퀴즈", layout="wide")

# 세션 상태 방어선 고정
if 'selected_apps' not in st.session_state: st.session_state.selected_apps = []
if 'duration_weeks' not in st.session_state: st.session_state.duration_weeks = 2
if 'schedule_matrix' not in st.session_state: st.session_state.schedule_matrix = None
if 'completed_days' not in st.session_state: st.session_state.completed_days = set()

# 어르신 전용 큰 글씨 및 스타일 디자인
st.markdown("""
    <style>
    html, body, [data-testid="stWidgetLabel"] p { font-size: 1.2rem !important; font-weight: bold !important; }
    h1 { font-size: 2.5rem !important; color: #1E3A8A; }
    h3 { font-size: 1.8rem !important; color: #1E40AF; }
    .stRadio [data-testid="stWidgetLabel"] p { font-size: 1.3rem !important; color: #334155; }
    div[data-testid="stMarkdownContainer"] p { font-size: 1.15rem; }
    </style>
""", unsafe_allow_html=True)

st.title("💯 4단계: 마무리 퀴즈 및 완료 도장 받기")
st.write("오늘 실전 실습을 잘 마치셨나요? 가벼운 퀴즈를 풀고 오늘 달력에 참 잘했어요 도장을 찍어보세요!")
st.markdown("---")

if st.session_state.schedule_matrix is None:
    st.warning("⚠️ 앞 단계에서 배우고 싶은 기능을 선택하고 스케줄표를 먼저 완성해 주세요!")
else:
    # 1. 주차 및 요일 선택 셀렉터
    weeks_list = list(range(1, st.session_state.duration_weeks + 1))
    days_list = ["월", "화", "수", "목", "금", "토", "일"]
    
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        selected_w = st.selectbox("📅 오늘의 [주차]를 고르세요:", weeks_list)
    with col_sel2:
        selected_d = st.selectbox("📆 오늘의 [요일]을 고르세요:", days_list)
        
    current_task = st.session_state.schedule_matrix[selected_w][selected_d]
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"📢 **오늘의 미션 확인:** `제 {selected_w}주차 {selected_d}요일 - {current_task}`")
    st.markdown("---")
    
    st.subheader("❓ 오늘의 디지털 마스터 확인 퀴즈")
    st.write("오늘 배운 내용입니다. 다음 중 올바른 행동이나 정답을 1~3번 중에서 하나 고르세요.")
    
    # 💡 기본값 문제 및 정답 인덱스 설정
    quiz_title = "Q. 오늘 배운 기능을 안전하게 사용하기 위한 올바른 방법은 무엇일까요?"
    options = [
        "1번: 잘 모르겠으면 화면 아무 곳이나 빠르게 연속으로 막 누른다.", 
        "2번: 안내 순서에 따라 글씨와 버튼을 천천히 눈으로 확인하며 누른다.", 
        "3번: 무서우니까 스마트폰을 그냥 즉시 꺼버린다."
    ]
    correct_idx = 1 
    
    # 키워드별 문제 동적 매칭
    if "똑닥" in current_task or "병원" in current_task:
        quiz_title = "Q. 똑닥 어플에서 원하는 병원을 찾고 싶을 때 가장 먼저 눌러야 하는 그림은 무엇일까요?"
        options = ["1번: 돋보기 모양 (검색창)", "2번: 쓰레기통 모양 (삭제)", "3번: 더하기 모양 (추가)"]
        correct_idx = 0
    elif "QR코드" in current_task or "처방전" in current_task:
        quiz_title = "Q. 스마트폰으로 종이 처방전의 QR코드를 인식시킬 때 올바른 자세는 무엇일까요?"
        options = [
            "1번: 스마트폰을 흔들며 카메라를 처방전에 바짝 비빈다.", 
            "2번: 카메라 사각형 점선 안에 QR코드가 쏙 들어오게 수평을 맞추고 2초간 멈춘다.", 
            "3번: 불을 다 끄고 어두운 방안에서 사진을 찍는다."
        ]
        correct_idx = 1
    elif "이체" in current_task or "용돈 보내기" in current_task:
        quiz_title = "Q. 은행 앱으로 돈을 보낼 때, 돈이 실제로 빠져나가기 직전 '가장 중요하게' 확인해야 할 것은?"
        options = [
            "1번: 스마트폰 배터리가 얼마나 남았는지 확인한다.", 
            "2번: 오늘 날씨가 맑은지 하늘을 확인한다.", 
            "3번: 화면에 뜬 '받는 사람 이름'과 '보낼 금액'이 맞는지 눈으로 재확인한다."
        ]
        correct_idx = 2
    elif "삼성페이" in current_task or "결제" in current_task:
        quiz_title = "Q. 스마트폰 간편결제를 할 때, 스마트폰의 어느 부위를 가게 카드 단말기에 대야 할까요?"
        options = ["1번: 스마트폰 화면 맨 앞면 유리창", "2번: 스마트폰의 아래쪽 충전 구멍", "3번: 스마트폰의 뒷면 중앙 부분"]
        correct_idx = 2
    elif "카카오T" in current_task or "택시" in current_task:
        quiz_title = "Q. 카카오T 앱에서 추가 요금 없이 가장 일반적이고 저렴하게 택시를 부르는 메뉴의 이름은?"
        options = ["1번: 모범 고급 호출", "2번: 일반 호출", "3번: 특급 대형 호출"]
        correct_idx = 1
    elif "유튜브" in current_task or "임영웅" in current_task:
        quiz_title = "Q. 유튜브에서 내가 좋아하는 가수의 노래를 검색창에 치고 난 후 눌러야 하는 자판 단추는?"
        options = ["1번: 돋보기 모양 (검색 단추)", "2번: 줄바꿈 모양 (엔터 단추)", "3번: 한영 변환 단추"]
        correct_idx = 0
    elif "사진 전송" in current_task or "카카오톡" in current_task:
        quiz_title = "Q. 카카오톡 대화방에서 상대방에게 내 사진을 전송하고 싶을 때 먼저 눌러야 하는 기호는?"
        options = ["1번: 물음표 기호 [?]", "2번: 더하기 모양 기호 [+]", "3번: 느낌표 기호 [!]"]
        correct_idx = 1
    elif "전화로 설명" in current_task or "혼자서" in current_task or "종이에" in current_task or "복습" in current_task:
        quiz_title = "Q. 오늘 진행한 '혼자 복습 및 응용 미션'의 가장 큰 핵심 목표는 무엇일까요?"
        options = [
            "1번: 남의 도움 없이 내 손 끝 감각으로 직접 다뤄보며 완전히 내 것으로 만들기", 
            "2번: 스마트폰을 새로 한 대 더 사러 대리점에 가기", 
            "3번: 어플이 어려우니까 앞으로 스마트폰을 절대 안 쓰기"
        ]
        correct_idx = 0

    # 💡 [컴파일러 에러 완벽 해결] 파이썬 3.14 컴파일 버전 호환성을 위해 구조를 완전 기초 안전형태로 변환
    user_choice = st.radio(quiz_title, options, index=0)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 정답 체크 판단 영역
    if user_choice:
        selected_answer_idx = options.index(user_choice)
        
        if selected_answer_idx == correct_idx:
            st.success("🎉 정답입니다! 아주 훌륭하십니다. 오늘 미션을 완벽하게 마스터하셨네요!")
            
            st.markdown("---")
            st.markdown("### 💮 5단계: 오늘 날짜에 참 잘했어요 도장 찍기")
            st.write("아래 큰 빨간 도장 단추를 누르시면 2단계 달력 계획표 화면에 '✅ 완료' 도장이 찍힙니다.")
            
            if st.button("💮 [여기를 꾹 누르면 오늘 공부 끝! 완료 도장 찍기]"):
                st.session_state.completed_days.add((selected_w, selected_d))
                st.balloons()
                st.success(f"⭕ 성공! 제 {selected_w}주차 {selected_d}요일 달력에 완료 도장을 쾅 찍었습니다! 내일 미션도 힘내세요!")
        else:
            st.error("❌ 아쉽게도 정답이 아닙니다! 다시 한번 천천히 읽어보시고 정답 번호를 골라보세요. 어르신은 하실 수 있습니다!")
