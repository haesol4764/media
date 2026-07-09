import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 기본 설정 및 내비게이션 구성
st.set_page_config(page_title="고령층 디지털 역량 강화 케어", layout="wide")

# 변경된 영문 파일명으로 매핑 (실제 파일 이름도 training.py, daily.py로 변경해야 합니다)
main_page = st.Page("main.py", title="홈 & 데이터 대시보드", icon="📊")
training_page = st.Page("training.py", title="맞춤형 훈련 스케줄러", icon="🎯")
daily_page = st.Page("daily.py", title="데일리 알림 & 실전 훈련", icon="📅")

# 내비게이션 바 생성
pg = st.navigation([main_page, training_page, daily_page])
pg.run()
