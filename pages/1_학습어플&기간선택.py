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
    div[data-testid="stHorizontalBlock"] { overflow: visible !important; }
    </style>
""", unsafe_allow_html=True)

# 💡 [핵심 해결책] 메인 파일 실행 시 모든 페이지에서 쓸 글로벌 세션 변수 미리 방어 생성
if 'selected_apps' not in st.session_state: st.session_state.selected_apps = []
if 'duration_weeks' not in st.session_state: st.session_state.duration_weeks = 2
if 'schedule_matrix' not in st.session_state: st.session_state.schedule_matrix = None
if 'completed_days' not in st.session_state: st.session_state.completed_days = set()

st.title("👵👴 시니어 디지털 소외 해소를 위한 플랫폼")
st.subheader("데이터 기반 맞춤형 스마트폰 자립 교육 솔루션")
st.markdown("---")

@st.cache_data
def load_data():
    df = pd.read_csv("countries_media.csv")
    df['이용행태별(1)'] = df['이용행태별(1)'].str.replace('"', '').str.strip()
    df['항목'] = df['항목'].str.strip()
    df['이용행태별(1)'] = df['이용행태별(1)'].str.replace('개인 정보', '개인정보')
    return df

try:
    df = load_data()
    st.markdown("### 📊 대한민국 고령층 디지털 정보화 실태 분석")
    
    categories = sorted(df['이용행태별(1)'].unique())
    selected_category = st.selectbox("🎯 분석하고 싶은 스마트폰 기능을 선택하세요", categories)
    
    cate_df = df[df['이용행태별(1)'] == selected_category].copy()
    
    # 연도별 데이터 보정 및 전처리
    processed_records = []
    for year in sorted(cate_df['시점'].unique()):
        year_df = cate_df[cate_df['시점'] == year]
        has_yes = year_df['항목'].str.contains('그렇다').any()
        
        if has_yes:
            yes_row = year_df[year_df['항목'].str.contains('그렇다')].iloc[0]
            val_60 = yes_row['만60-69세']
            val_70 = yes_row['만70세이상']
        else:
            has_no = year_df['항목'].str.contains('그렇지 않다').any()
            if has_no:
                no_row = year_df[year_df['항목'].str.contains('그렇지 않다')].iloc[0]
                val_60 = round(100 - no_row['만60-69세'], 1)
                val_70 = round(100 - no_row['만70세이상'], 1)
            else:
                val_60, val_70 = 0.0, 0.0
                
        processed_records.append({
            '시점': f"{year}년", '만60-69세': val_60, '만70세이상': val_70, '이용행태별(1)': selected_category
        })
        
    trend_df = pd.DataFrame(processed_records)
    
    if not trend_df.empty:
        latest_row = trend_df.iloc[-1]
        st.markdown(f"#### 💡 최신 조사 결과 기준 역량 수준 ({latest_row['시점']})")
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric(label="만 60 ~ 69세 수행 가능 비율", value=f"{latest_row['만60-69세']}%")
        with col_m2:
            st.metric(label="만 70세 이상 수행 가능 비율", value=f"{latest_row['만70세이상']}%")
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 📈 연도별 정보화 역량 추이 그래프")
        if not trend_df.empty:
            fig_line = px.line(trend_df, x='시점', y=['만60-69세', '만70세이상'],
                               labels={'value': '가능 비율 (%)', '시점': '조사 연도', 'variable': '연령대'},
                               markers=True, title=f"[{selected_category}] 연도별 추이")
            fig_line.update_layout(autosize=True, margin=dict(l=40, r=40, t=40, b=40), xaxis={'type': 'category'})
            st.plotly_chart(fig_line, use_container_width=True, config={'responsive': True})
            
    with col2:
        st.markdown("#### 🎯 연도별 연령층 간 분포도")
        if not cate_df.empty:
            cate_df['시점'] = cate_df['시점'].astype(str) + "년"
            fig_scatter = px.scatter(cate_df, x='만60-69세', y='만70세이상', color='항목',
                                     hover_data=['시점'], title="연령층 간 점수 분포 비율")
            fig_scatter.update_traces(marker=dict(size=14, line=dict(width=1, color='DarkSlateGrey')))
            fig_scatter.update_layout(autosize=True, margin=dict(l=40, r=40, t=40, b=40))
            st.plotly_chart(fig_scatter, use_container_width=True, config={'responsive': True})
        
    st.markdown("---")
    st.info("💡 통계를 확인하셨다면 왼쪽 메뉴에서 **'1 학습 어플 및 기간 선택'**을 눌러 진행하세요!")
except Exception as e:
    st.error(f"🚨 파일을 불러올 수 없거나 에러가 발생했습니다: {e}")
