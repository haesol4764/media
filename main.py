import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="시니어 디지털 마스터", layout="wide")

# 스타일 보완 (글씨 크기 및 차트 컨테이너 안정화)
st.markdown("""
    <style>
    html, body, [data-testid="stWidgetLabel"] p { font-size: 1.15rem !important; font-weight: bold !important; }
    h1 { font-size: 2.6rem !important; color: #1E3A8A; }
    h2 { font-size: 2.0rem !important; color: #0D9488; }
    div[data-testid="stHorizontalBlock"] { overflow: visible !important; } /* 화면 잘림 방지 */
    </style>
""", unsafe_allow_html=True)

st.title("👵👴 시니어 디지털 소외 해소를 위한 플랫폼")
st.subheader("데이터 기반 맞춤형 스마트폰 자립 교육 솔루션")
st.markdown("---")

# 데이터 로드 및 전처리 (공백 및 따옴표 제거로 매칭 오류 원천 차단)
@st.cache_data
def load_data():
    df = pd.read_csv("countries_media.csv")
    # 텍스트 데이터 정제
    df['이용행태별(1)'] = df['이용행태별(1)'].str.replace('"', '').str.strip()
    df['항목'] = df['항목'].str.strip()
    return df

try:
    df = load_data()
    
    st.markdown("### 📊 대한민국 고령층 디지털 정보화 실태 분석")
    
    # 정제된 카테고리 목록 정렬하여 가져오기
    categories = sorted(df['이용행태별(1)'].unique())
    selected_category = st.selectbox("🎯 분석하고 싶은 스마트폰 기능을 선택하세요", categories)
    
    # 선택한 카테고리에 맞는 데이터 필터링
    cate_df = df[df['이용행태별(1)'] == selected_category]
    
    # '그렇다' 혹은 '그렇지 않다'를 유연하게 포괄하기 위해 필터 개선
    yes_trend = cate_df[cate_df['항목'].str.contains('그렇다|인도|확인|가능|인지')] 
    
    # 1. 주요 지표 요약 카드 (가장 최신 시점 데이터 가져오기)
    if not cate_df.empty:
        latest_year = cate_df['시점'].max()
        latest_df = cate_df[cate_df['시점'] == latest_year]
        
        if not latest_df.empty:
            st.markdown(f"#### 💡 가장 최근 조사 결과 ({latest_year}년 기준 - {latest_df.iloc[0]['항목']})")
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                val_60 = latest_df.iloc[0]['만60-69세']
                st.metric(label="만 60 ~ 69세 역량 수준", value=f"{val_60}%")
            with col_m2:
                val_70 = latest_df.iloc[0]['만70세이상']
                st.metric(label="만 70세 이상 역량 수준", value=f"{val_70}%")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2. 입체적 시각화 (영역 차트 & 산점도)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 연도별 정보화 역량 추이 그래프")
        if not yes_trend.empty:
            # 안전하게 시점 순으로 정렬 후 시각화
            yes_trend = yes_trend.sort_values('시점')
            
            fig_area = px.area(yes_trend, x='시점', y=['만60-69세', '만70세이상'],
                               labels={'value': '비율 (%)', '시점': '조사 연도', 'variable': '연령대'},
                               line_shape='spline', title=f"[{selected_category}] 추이")
            
            # 차트 여백 및 반응형 깨짐 방지 설정 추가
            fig_area.update_layout(autosize=True, margin=dict(l=40, r=40, t=40, b=40))
            st.plotly_chart(fig_area, use_container_width=True, config={'responsive': True})
        else:
            st.info("ℹ️ 해당 문항은 추이 데이터가 없거나 항목 분석 중입니다.")
            
    with col2:
        st.markdown("#### 🎯 연도별 연령층 간 분포도")
        if not cate_df.empty:
            # 데이터 개수가 적어도 흩어짐을 볼 수 있도록 산점도 마커 크기 최적화 고정
            fig_scatter = px.scatter(cate_df, x='만60-69세', y='만70세이상', color='항목',
                                     hover_data=['시점'], title="연령층 간 점수 분포 비율",
                                     labels={'만60-69세': '60대 비율 (%)', '만70세이상': '70대 이상 비율 (%)'})
            
            # 마커 크기 고정 및 사라짐 방지 설정
            fig_scatter.update_traces(marker=dict(size=14, line=dict(width=1, color='DarkSlateGrey')))
            fig_scatter.update_layout(autosize=True, margin=dict(l=40, r=40, t=40, b=40))
            st.plotly_chart(fig_scatter, use_container_width=True, config={'responsive': True})
        else:
            st.info("ℹ️ 분포도를 그릴 데이터가 부족합니다.")
        
    st.markdown("---")
    st.info("💡 통계를 확인하셨다면 왼쪽 메뉴에서 **'1_학습_어플_및_기간_선택'**을 눌러 다음 단계로 진행하세요!")

except Exception as e:
    st.error(f"🚨 오류가 발생했습니다. 개발자 로그를 확인하세요. (에러 내용: {e})")
