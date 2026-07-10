import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="시니어 디지털 마스터", layout="wide")

# 어르신 및 사용자용 공통 스타일 적용
st.markdown("""
    <style>
    html, body, [data-testid="stWidgetLabel"] p { font-size: 1.15rem !important; font-weight: bold !important; }
    h1 { font-size: 2.6rem !important; color: #1E3A8A; }
    h2 { font-size: 2.0rem !important; color: #0D9488; }
    .metric-box { background-color: #F0FDF4; padding: 15px; border-radius: 10px; border: 1px solid #BBF7D0; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.title("👵👴 시니어 디지털 소외 해소 플랫폼")
st.subheader("데이터 기반 맞춤형 스마트폰 자립 교육 솔루션")
st.markdown("---")

# 데이터 로드
@st.cache_data
def load_data():
    return pd.read_csv("countries_media.csv")

try:
    df = load_data()
    
    # 1. 상단 드롭다운 필터링 UI
    st.markdown("### 📊 대한민국 고령층 디지털 정보화 실태 분석")
    categories = df['이용행태별(1)'].unique()
    selected_category = st.selectbox("🎯 분석하고 싶은 스마트폰 기능을 선택하세요", categories)
    
    # 데이터 필터링
    cate_df = df[df['이용행태별(1)'] == selected_category]
    yes_trend = cate_df[cate_df['항목'].str.contains('그렇다')]
    no_trend = cate_df[cate_df['항목'].str.contains('그렇지 않다')]
    
    # 2. 주요 지표 요약 카드 (Metric)
    latest_df = cate_df[cate_df['시점'] == 2024]
    if not latest_df.empty:
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            val_60 = latest_df.iloc[0]['만60-69세']
            st.metric(label=f"2024년 만60-69세의 능력 수준 ({latest_df.iloc[0]['항목']})", value=f"{val_60}%")
        with col_m2:
            val_70 = latest_df.iloc[0]['만70세이상']
            st.metric(label=f"2024년 만70세 이상 능력 수준 ({latest_df.iloc[0]['항목']})", value=f"{val_70}%")
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 3. 입체적 시각화 (영역 차트 & 산점도)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 연도별 '할 수 있다(그렇다)' 응답 추이")
        # 영역 차트 (Area Chart) 사용으로 심심함 탈피
        fig_area = px.area(yes_trend, x='시점', y=['만60-69세', '만70세이상'],
                           labels={'value': '비율 (%)', '시점': '조사 연도'},
                           line_shape='spline', title="연도별 역량 강화 트렌드")
        st.plotly_chart(fig_area, use_container_width=True)
        
    with col2:
        st.markdown("#### 🎯 연도별 연령층 간 격차 분포")
        # 산점도 차트 (Scatter Plot) 및 추세선 묘사
        fig_scatter = px.scatter(cate_df, x='만60-69세', y='만70세이상', color='항목', size='시점',
                                 hover_data=['시점'], title="연령층 간 상관관계 및 분포도",
                                 labels={'만60-69세': '60대 비율 (%)', '만70세이상': '70대 이상 비율 (%)'})
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    st.markdown("---")
    st.info("💡 통계를 확인하셨다면 왼쪽 사이드바 메뉴에서 **'1_학습_어플_및_기간_선택'**을 눌러 맞춤 스케줄러 제작을 시작하세요!")

except Exception as e:
    st.error("🚨 'countries_media.csv' 파일이 main.py와 같은 폴더에 있는지 확인해주세요.")
