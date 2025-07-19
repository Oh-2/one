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

# ✅ 각 지역의 평균을 새로운 열로 추가
df_top5_with_avg_col = df_top5.copy()
df_top5_with_avg_col["평균"] = df_top5.mean(axis=1)

# ✅ 열 순서 조정: "평균" 열을 맨 앞으로
cols = df_top5_with_avg_col.columns.tolist()
cols = ["평균"] + [col for col in cols if col != "평균"]
df_top5_with_avg_col = df_top5_with_avg_col[cols]

# 📄 상위 5개 지역 + 평균 열 표시
st.subheader("📄 평균 강수량 상위 5개 지역 (지역별 평균 포함)")
st.dataframe(df_top5_with_avg_col)

# 🌧️ 선 그래프 (변경 없음)
df_chart = df_top5.T
st.subheader("🌧️ 연도별 강수량 변화 (상위 5개 지역)")
st.line_chart(df_chart)

st.caption("※ 강수량 단위는 mm로 가정합니다.")
