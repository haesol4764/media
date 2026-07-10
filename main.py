import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="시니어 디지털 마스터", layout="wide")

# 스타일 보완
st.markdown("""
    <style>
    html, body, [data-testid="stWidgetLabel"] p { font-size: 1.15rem !important; font-weight: bold !important; }
    h1 { font-size: 2.6rem !important; color: #1E3A8A; }
    h2 { font-size: 2.0rem !important; color: #0D9488; }
    div[data-testid="stHorizontalBlock"] { overflow: visible !important; }
    </style>
""", unsafe_allow_html=True)

st.title("👵👴 시니어 디지털 소외 해소를 위한 플랫폼")
st.subheader("데이터 기반 맞춤형 스마트폰 자립 교육 솔루션")
st.markdown("---")

@st.cache_data
def load_data():
    df = pd.read_csv("countries_media.csv")
    df['이용행태별(1)'] = df['이용행태별(1)'].str.replace('"', '').str.strip()
    df['항목'] = df['항목'].str.strip()
    
    # [핵심 수정 1] 시점(연도)을 숫자가 아닌 '텍스트'로 변경하여 축 왜곡 방지
    df = df.sort_values('시점')
    df['시점'] = df['시점'].astype(str) + "년"
    return df

try:
    df = load_data()
    
    st.markdown("### 📊 대한민국 고령층 디지털 정보화 실태 분석")
    
    categories = sorted(df['이용행태별(1)'].unique())
    selected_category = st.selectbox("🎯 분석하고 싶은 스마트폰 기능을 선택하세요", categories)
    
    cate_df = df[df['이용행태별(1)'] == selected_category]
    
    # [핵심 수정 2] '그렇다' 문구가 포함된 긍정 지표 데이터만 정확하게 필터링
    yes_trend = cate_df[cate_df['항목'].str.contains('그렇다')] 
    
    # 1. 주요 지표 요약 카드
    if not cate_df.empty:
        latest_df = cate_df.tail(1) # 가장 마지막에 있는 최신 데이터 추출
        
        st.markdown(f"#### 💡 최신 조사 결과 기준 역량 수준")
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            val_60 = latest_df.iloc[0]['만60-69세']
            st.metric(label=f"만 60 ~ 69세 ({latest_df.iloc[0]['시점']})", value=f"{val_60}%")
        with col_m2:
            val_70 = latest_df.iloc[0]['만70세이상']
            st.metric(label=f"만 70세 이상 ({latest_df.iloc[0]['시점']})", value=f"{val_70}%")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2. 시각화 영역 (라인 차트 & 산점도)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 연도별 정보화 역량 추이 그래프")
        if not yes_trend.empty:
            # [핵심 수정 3] px.area 대신 데이터 공백에 강한 px.line 사용 + 마커(점) 표시
            fig_line = px.line(yes_trend, x='시점', y=['만60-69세', '만70세이상'],
                               labels={'value': '비율 (%)', '시점': '조사 연도', 'variable': '연령대'},
                               markers=True, title=f"[{selected_category}] 연도별 추이")
            
            # 그래프가 옆으로 밀려도 안 깨지게 레이아웃 고정
            fig_line.update_layout(autosize=True, margin=dict(l=40, r=40, t=40, b=40), xaxis={'type': 'category'})
            st.plotly_chart(fig_line, use_container_width=True, config={'responsive': True})
        else:
            st.info("ℹ️ 해당 문항은 '그렇다' 기준의 추이 데이터가 없습니다.")
            
    with col2:
        st.markdown("#### 🎯 연도별 연령층 간 분포도")
        if not cate_df.empty:
            fig_scatter = px.scatter(cate_df, x='만60-69세', y='만70세이상', color='항목',
                                     hover_data=['시점'], title="연령층 간 점수 분포 비율",
                                     labels={'만60-69세': '60대 비율 (%)', '만70세이상': '70대 이상 비율 (%)'})
            
            fig_scatter.update_traces(marker=dict(size=14, line=dict(width=1, color='DarkSlateGrey')))
            fig_scatter.update_layout(autosize=True, margin=dict(l=40, r=40, t=40, b=40))
            st.plotly_chart(fig_scatter, use_container_width=True, config={'responsive': True})
        else:
            st.info("ℹ️ 분포도를 그릴 데이터가 부족합니다.")
        
    st.markdown("---")
    st.info("💡 통계를 확인하셨다면 왼쪽 메뉴에서 **'1_학습_어플_및_기간_선택'**을 눌러 다음 단계로 진행하세요!")

except Exception as e:
    st.error(f"🚨 오류가 발생했습니다: {e}")
