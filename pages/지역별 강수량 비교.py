import streamlit as st
import pandas as pd

st.set_page_config(page_title="강수량 분석", layout="wide")
st.title("📊 강수량 데이터 분석")

# CSV 파일 불러오기 (첫 번째 행 = 연도, 첫 번째 열 = 지역명)
file_path = "강수량.csv"
try:
    df = pd.read_csv(file_path, encoding='euc-kr')
except FileNotFoundError:
    st.error("❌ '강수량.csv' 파일을 찾을 수 없습니다. 앱과 같은 폴더에 넣어주세요.")
    st.stop()

# 첫 번째 열을 '지역'으로 설정 (index로 사용)
df = df.rename(columns={df.columns[0]: "지역"})
df = df.set_index("지역")

# 열 이름이 연도이므로 숫자형 문자열로 변환
df.columns = df.columns.astype(str)

# 숫자형으로 변환
df = df.apply(pd.to_numeric, errors='coerce')

# 평균값 기준 상위 5개 지역 추출
mean_precip = df.mean(axis=1)
top5_regions = mean_precip.sort_values(ascending=False).head(5).index
df_top5 = df.loc[top5_regions]

# 선 그래프 시각화를 위한 전치 (연도가 가로축, 지역이 컬럼)
df_top5_transposed = df_top5.T

# 📄 상위 5개 지역 데이터 표시
st.subheader("📄 평균 강수량 상위 5개 지역")
st.dataframe(df_top5)

# 🌧️ 선 그래프 시각화
st.subheader("🌧️ 연도별 강수량 변화 (상위 5개 지역)")
st.line_chart(df_top5_transposed)

# 참고
st.caption("※ 강수량 단위는 mm로 가정합니다.")

