import streamlit as st
import pandas as pd

st.set_page_config(page_title="강수량 분석", layout="wide")
st.title("📊 강수량 데이터 분석")

# CSV 불러오기 (EUC-KR 인코딩, 연도 = 인덱스)
file_path = "강수량.csv"
try:
    df = pd.read_csv(file_path, encoding='euc-kr', index_col=0)
except FileNotFoundError:
    st.error("❌ '강수량.csv' 파일이 존재하지 않습니다. 앱과 같은 폴더에 넣어주세요.")
    st.stop()

# 데이터 전치: 지역을 행으로, 연도를 열로
df = df.T
df.columns = df.columns.astype(str)
df = df.apply(pd.to_numeric, errors='coerce')

# 평균값 기준 상위 5개 지역 추출
mean_precip = df.mean(axis=1)
top5_regions = mean_precip.sort_values(ascending=False).head(5).index
df_top5 = df.loc[top5_regions]

# 평균 행 추가
df_top5_with_avg = df_top5.copy()
df_top5_with_avg.loc["평균"] = df_top5.mean()

# 📄 상위 5개 지역 + 평균값 표시
st.subheader("📄 평균 강수량 상위 5개 지역 + 평균")
st.dataframe(df_top5_with_avg)

# 🌧️ 연도별 선 그래프 (평균 제외)
st.subheader("🌧️ 연도별 강수량 변화 (상위 5개 지역)")
st.line_chart(df_top5.T)

st.caption("※ 강수량 단위는 mm로 가정합니다.")

