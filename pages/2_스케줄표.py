import streamlit as st

st.set_page_config(page_title="2단계: 주간 달력", layout="wide")

st.title("📅 나만의 한눈에 보는 가로 달력 계획표")
st.write("완료 체크를 마친 날은 달력 칸이 초록색으로 바뀝니다.")
st.markdown("---")

if 'schedule_matrix' not in st.session_state or not st.session_state.schedule_matrix:
    st.warning("⚠️ 1단계에서 어플과 기간을 선택한 후 큰 버튼을 누르셔야 달력이 나타납니다!")
else:
    weeks = st.session_state.duration_weeks
    days_list = ["월", "화", "수", "목", "금", "토", "일"]
    
    total_slots = weeks * 7
    done_slots = len(st.session_state.completed_days)
    progress_percent = int((done_slots / total_slots) * 100)
    
    st.subheader(f"🏆 현재 어르신의 디지털 마스터 진도율: {progress_percent}% 완료")
    st.progress(done_slots / total_slots)
    
    for w in range(1, weeks + 1):
        st.markdown(f"### 🗓️ [ 제 {w} 주 차 ] 학습 달력")
        cols = st.columns(7)
        
        for idx, d in enumerate(days_list):
            with cols[idx]:
                is_done = (w, d) in st.session_state.completed_days
                task_text = st.session_state.schedule_matrix[w][d]
                
                if is_done:
                    box_style = "background-color: #DCFCE7; border: 2px solid #22C55E; color: #166534;"
                    badge = "✅ 완료"
                else:
                    box_style = "background-color: #FFFBEB; border: 2px solid #F59E0B; color: #78350F;"
                    badge = "⏳ 대기"
                    
                st.markdown(f"""
                    <div style="{box_style} padding: 12px; border-radius: 8px; min-height: 140px; font-size: 0.95rem;">
                        <center><b>{d}요일 ({badge})</b></center>
                        <hr style='margin:6px 0; border: 0.5px solid #ccc;'>
                        {task_text[:40]}...
                    </div>
                """, unsafe_allow_html=True)
