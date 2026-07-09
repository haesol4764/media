import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 기본 설정 및 내비게이션 구성
st.set_page_config(page_title="고령층 디지털 역량 강화 케어", layout="wide")

# 페이지 정의
main_page = st.Page("main.py", title="홈 & 데이터 대시보드", icon="📊")
training_page = st.Page("개인별맞춤훈련선택.py", title="맞춤형 훈련 스케줄러", icon="🎯")
daily_page = st.Page("데일리알림및훈련.py", title="데일리 알림 & 실전 훈련", icon="📅")

# 내비게이션 바 생성
pg = st.navigation([main_page, training_page, daily_page])
pg.run()

# --- 메인 페이지 콘텐츠 (현재 파일이 실행될 때만 표시) ---
if st.get_option("client.showErrorDetails"): # 내비게이션 실행 후 메인 콘텐츠 분기
    pass

# 실제 main.py의 콘텐츠 표시는 아래와 같이 처리하거나, 
# st.navigation 구조상 안전하게 현재 페이지 이름을 체크하여 렌더링합니다.
if st.experimental_user.get("current_page") == "main.py" or True:
    st.title("👵👴 고령층 디지털 소외 해소를 위한 맞춤형 훈련 플랫폼")
    st.write("""
    본 플랫폼은 **'countries_media.csv'** 데이터를 기반으로, 만 60세 이상 시니어 계층의 디지털 기기 기능별 활용 현황을 분석하고, 
    어르신들이 디지털 세상에 쉽게 적응할 수 있도록 **개인 맞춤형 훈련 스케줄과 데일리 미션**을 제공합니다.
    """)
    
    st.markdown("---")
    
    # 데이터 로드
    @st.cache_data
    def load_data():
        df = pd.read_csv("countries_media.csv")
        return df

    try:
        df = load_data()
        
        st.subheader("📈 시니어 디지털 정보화 수준 분석 대시보드")
        
        # 필터 선택
        years = df['시점'].unique()
        selected_year = st.selectbox("🎯 분석 년도 선택", years)
        
        filtered_df = df[df['시점'] == selected_year]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"#### 👍 잘하시는 분야 ('그렇다' 비율이 높은 순)")
            yes_df = filtered_df[filtered_df['항목'].str.contains('그렇다')]
            # 만60-69세 기준으로 정렬하여 상위 5개 추출
            top_5 = yes_df.sort_values(by='만60-69세', ascending=False).head(5)
            
            fig_top = px.bar(top_5, x='이용행태별(1)', y=['만60-69세', '만70세이상'],
                             barmode='group', title="상위 5개 디지털 역량 (%)",
                             labels={'value': '비율 (%)', '이용행태별(1)': '디지털 기능'})
            st.plotly_chart(fig_top, use_container_width=True)
            
        with col2:
            st.markdown(f"#### ⚠️ 도움이 필요한 분야 ('그렇지 않다' 비율이 높은 순)")
            no_df = filtered_df[filtered_df['항목'].str.contains('그렇지 않다')]
            bottom_5 = no_df.sort_values(by='만60-69세', ascending=False).head(5)
            
            fig_bottom = px.bar(bottom_5, x='이용행태별(1)', y=['만60-69세', '만70세이상'],
                                 barmode='group', title="하위 5개 디지털 역량 (어려움 체감 %)",
                                 labels={'value': '비율 (%)', '이용행태별(1)': '디지털 기능'})
            st.plotly_chart(fig_bottom, use_container_width=True)
            
        st.markdown("### 📋 전체 데이터 분석 테이블")
        st.dataframe(filtered_df, use_container_width=True)
        
    except FileNotFoundError:
        st.error("🚨 'countries_media.csv' 파일을 찾을 수 없습니다. 파일 경로를 확인해주세요.")
