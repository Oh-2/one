import streamlit as st
import pandas as pd

st.set_page_config(page_title="강수량 분석", layout="wide")
st.title("📊 강수량 데이터 분석")

# CSV 파일 불러오기 (EUC-KR 인코딩, 헤더 없이)
file_path = "강수량.csv"
try:
    raw_df = pd.read_csv(file_path, encoding='euc-kr', header=None)
except FileNotFoundError:
    st.error("❌ '강수량.csv' 파일을 찾을 수 없습니다. 앱과 같은 폴더에 파일을 넣어주세요.")
    st.stop()

# 첫 행을 열 이름으로 설정 (연도), 첫 열은 지역
raw_df.columns = raw_df.iloc[0]
df = raw_df.drop(index=0)

# 첫 번째 열을 지역 이름으로 설정
df = df.set_index(df.columns[0])

# 숫자형으로 변환
df = df.apply(pd.to_numeric, errors='coerce')

# 평균값 기준 상위 5개 지역 추출
mean_precip = df.mean(axis=1)
top5_regions = mean_precip.sort_values(ascending=False).head(5).index
df_top5 = df.loc[top5_regions]

# 시각화를 위해 전치 (연도가 가로축)
df_top5_transposed = df_top5.T

# 📄 상위 5개 지역 데이터 표시
st.subheader("📄 상위 5개 지역 원본 데이터")
st.dataframe(df_top5)

# 🌧️ 선 그래프 표시
st.subheader("🌧️ 연도별 강수량 변화 (상위 5개 지역)")
st.line_chart(df_top5_transposed)

st.caption("※ 강수량 단위는 mm로 가정합니다.")
