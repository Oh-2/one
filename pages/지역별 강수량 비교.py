import streamlit as st
import pandas as pd

st.set_page_config(page_title="강수량 분석", layout="wide")
st.title("📊 강수량 데이터 분석")

# CSV 불러오기 (EUC-KR 인코딩)
file_path = "강수량.csv"
try:
    df = pd.read_csv(file_path, encoding='euc-kr', index_col=0)
except FileNotFoundError:
    st.error("❌ '강수량.csv' 파일이 존재하지 않습니다. 앱과 같은 폴더에 넣어주세요.")
    st.stop()

# 데이터 형태: 연도(행) x 지역(열) → 전치
df = df.T

# 열 이름(연도)을 문자열로 통일
df.columns = df.columns.astype(str)

# 모든 값을 숫자로 변환 (결측치는 NaN)
df = df.apply(pd.to_numeric, errors='coerce')

# 평균값 기준 상위 5개 지역 추출
mean_precip = df.mean(axis=1)
top5_regions = mean_precip.sort_values(ascending=False).head(5).index
df_top5 = df.loc[top5_regions]

# 시각화를 위해 전치: 연도별 강수량 변화 (가로축: 연도, 선: 지역)
df_top5_transposed = df_top5.T

# 📄 원본 데이터 표시 (상위 5개 지역만)
st.subheader("📄 평균 강수량 상위 5개 지역")
st.dataframe(df_top5)

# 🌧️ 선 그래프 표시
st.subheader("🌧️ 연도별 강수량 변화 (상위 5개 지역)")
st.line_chart(df_top5_transposed)

# 안내
st.caption("※ 강수량 단위는 mm로 가정합니다.")

