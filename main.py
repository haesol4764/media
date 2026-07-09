import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. 현재 main.py가 위치한 폴더의 절대 경로 추출
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. 페이지 기본 설정
st.set_page_config(page_title="고령층 디지털 역량 강화 케어", layout="wide")

# 3. os.path.join을 사용하여 파일의 절대 경로를 Streamlit에 전달
main_page = st.Page(os.path.join(current_dir, "main.py"), title="홈 & 데이터 대시보드", icon="📊")
training_page = st.Page(os.path.join(current_dir, "training.py"), title="맞춤형 훈련 스케줄러", icon="🎯")
daily_page = st.Page(os.path.join(current_dir, "daily.py"), title="데일리 알림 & 실전 훈련", icon="📅")

# 내비게이션 바 생성 및 실행
pg = st.navigation([main_page, training_page, daily_page])
pg.run()

# --- 이하 대시보드 및 데이터 분석 코드 동일 ---
