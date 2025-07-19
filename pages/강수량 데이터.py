import streamlit as st
import pandas as pd

st.set_page_config(page_title="강수량 분석", layout="wide")
st.title("📊 강수량 데이터 분석")

# 1. CSV 파일 불러오기 (EUC-KR 인코딩, 연도 = 행)
file_path = "강수량.csv"
try:
    df = pd.read_csv(file_path, encoding='euc-kr', index_col=0)
except FileNotFoundError:
    st.error("❌ '강수량.csv' 파일이 존재하지 않습니다. 앱과 같은 폴더에 넣어주세요.")
    st.stop()

# 2. 전치하여: 지역 = 행, 연도 = 열
df = df.T
df.columns = df.columns.astype(str)
df = df.apply(pd.to_numeric, errors='coerce')

# 3. 평균 기준 상위 5개 지역 추출
mean_precip = df.mean(axis=1)
top5_regions = mean_precip.sort_values(ascending=False).head(5).index
df_top5 = df.loc[top5_regions]

# 4. 원본 데이터에 평균 열 추가 (맨 앞에 배치)
df_top5_with_avg_col = df_top5.copy()
df_top5_with_avg_col["평균"] = df_top5.mean(axis=1)
cols = df_top5_with_avg_col.columns.tolist()
cols = ["평균"] + [col for col in cols if col != "평균"]
df_top5_with_avg_col = df_top5_with_avg_col[cols]

# 5. 📄 데이터 출력
st.subheader("📄 평균 강수량 상위 5개 지역")
st.dataframe(df_top5_with_avg_col)

# 6. 🌧️ 지역별 단일 선 그래프
st.subheader("🌧️ 연도별 강수량 변화 (지역별 그래프)")

df_chart = df_top5.T  # 연도 = index, 지역 = column

for region in df_chart.columns:
    st.markdown(f"#### 📍 {region}")
    st.line_chart(df_chart[[region]])  # 각 지역에 대해 하나씩 선 그래프 출력

# 7. 안내
st.caption("※ 강수량 단위는 mm로 가정합니다.")
