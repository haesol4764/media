import streamlit as st

st.set_page_config(page_title="3단계: 주간 달력", layout="wide")

# 세션 상태 유지 및 데이터 방어선 고정
if 'selected_apps' not in st.session_state: st.session_state.selected_apps = []
if 'duration_weeks' not in st.session_state: st.session_state.duration_weeks = 2
if 'schedule_matrix' not in st.session_state: st.session_state.schedule_matrix = None
if 'completed_days' not in st.session_state: st.session_state.completed_days = set()

# 스타일 설정 (어르신 맞춤형 큰 글씨)
st.markdown("""
    <style>
    html, body, [data-testid="stWidgetLabel"] p { font-size: 1.15rem !important; font-weight: bold !important; }
    h1 { font-size: 2.5rem !important; color: #1E3A8A; }
    h3 { font-size: 1.8rem !important; color: #1E40AF; margin-top: 20px !important; }
    </style>
""", unsafe_allow_html=True)

st.title("📅 나만의 한눈에 보는 가로 달력 계획표")
st.write("1단계에서 선택하신 기간에 맞춰 매일 새로운 맞춤형 미션이 분배되었습니다.")
st.markdown("---")

# 기능별 이쁜 색상 매칭 함수 (어르신 가독성 최적화)
def get_box_style(task_text, is_done):
    # 만약 완료 도장을 찍은 날이라면 무조건 초록색으로 변경
    if is_done:
        return "background-color: #DCFCE7; border: 3px solid #22C55E; color: #15803D;"
        
    # 미션 카테고리별 파스텔톤 색상 지정
    if "[병원]" in task_text or "[약국]" in task_text:
        return "background-color: #EFF6FF; border: 2px solid #3B82F6; color: #1E40AF;" # 파란색 계열
    elif "[금융]" in task_text:
        return "background-color: #FEF9C3; border: 2px solid #EAB308; color: #854D0E;" # 노란색 계열
    elif "[교통]" in task_text:
        return "background-color: #F5F3FF; border: 2px solid #8B5CF6; color: #5B21B6;" # 보라색 계열
    elif "[쇼핑]" in task_text or "[생활]" in task_text:
        return "background-color: #FFEDD5; border: 2px solid #F97316; color: #9A3412;" # 주황색 계열
    elif "[소통]" in task_text or "[여가]" in task_text:
        return "background-color: #FDF2F8; border: 2px solid #EC4899; color: #9D174D;" # 핑크색 계열
    elif "[기본]" in task_text or "[보안]" in task_text:
        return "background-color: #F0FDF4; border: 2px solid #4ADE80; color: #166534;" # 연두색 계열
    else:
        return "background-color: #FAFAFA; border: 2px solid #737373; color: #404040;" # 기본 회색 계열

if st.session_state.schedule_matrix is None:
    st.warning("⚠️ 1단계 '학습 어플 및 기간 선택' 메뉴에서 배울 어플을 고른 후 [스케줄표 생성] 큰 버튼을 먼저 눌러주셔야 이 달력이 나타납니다!")
else:
    weeks = st.session_state.duration_weeks
    days_list = ["월", "화", "수", "목", "금", "토", "일"]
    
    # 상단 전체 진도율 바 표시
    total_slots = weeks * 7
    done_slots = len(st.session_state.completed_days)
    progress_percent = int((done_slots / total_slots) * 100)
    
    st.subheader(f"🏆 현재 어르신의 디지털 마스터 진도율: {progress_percent}% 완료")
    st.progress(done_slots / total_slots)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 주차별 가로 달력 렌더링
    for w in range(1, weeks + 1):
        st.markdown(f"### 🗓️ [ 제 {w} 주 차 ] 매일 다르게 배우는 달력")
        cols = st.columns(7)
        
        for idx, d in enumerate(days_list):
            with cols[idx]:
                # 해당 주차/요일에 배정된 텍스트 추출
                task_text = st.session_state.schedule_matrix[w][d]
                is_done = (w, d) in st.session_state.completed_days
                
                # 상단 배지 상태 정의
                badge = "✅ 완료" if is_done else "⏳ 오늘미션"
                
                # 동적 박스 디자인 바인딩
                box_design = get_box_style(task_text, is_done)
                
                # 가로 칸 디자인 출력
                st.markdown(f"""
                    <div style="{box_design} padding: 14px; border-radius: 12px; min-height: 170px; font-size: 1.0rem; box-shadow: 1px 2px 5px rgba(0,0,0,0.05);">
                        <center><span style="font-size: 1.1rem;"><b>{d}요일</b></span> <br> <small>({badge})</small></center>
                        <hr style='margin: 8px 0; border: 0.5px solid opacity 0.3;'>
                        <div style="line-height: 1.4;">{task_text}</div>
                    </div>
                """, unsafe_allow_html=True)
                
    st.markdown("---")
    st.info("💡 오늘 요일의 미션을 눈으로 확인하셨다면, 왼쪽 메뉴의 **'3 데일리 알림 및 실전 가이드'**로 이동하여 실제 스마트폰 훈련을 시작하세요!")
