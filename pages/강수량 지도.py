import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(page_title="강수량 분석 지도", layout="wide")
st.title("🗺️ 강수량 데이터 지도 시각화")

# 1. CSV 파일 불러오기 (EUC-KR 인코딩, 연도 = 행)
file_path = "강수량.csv"
try:
    df = pd.read_csv(file_path, encoding='euc-kr', index_col=0)
except FileNotFoundError:
    st.error("❌ '강수량.csv' 파일이 존재하지 않습니다. 앱과 같은 폴더에 넣어주세요.")
    st.stop()

# 2. 전치: 지역 = 행, 연도 = 열
df = df.T
df.columns = df.columns.astype(str)
df = df.apply(pd.to_numeric, errors='coerce')

# 3. 평균 기준 상위 5개 지역 추출
mean_precip = df.mean(axis=1)
top5_regions = mean_precip.sort_values(ascending=False).head(5).index
df_top5 = df.loc[top5_regions]
region_means = df_top5.mean(axis=1)

# 4. 지역별 위도/경도 정보 (수동 입력)
region_coords = {
    "제주특별자치도 성산": (33.3868, 126.8807),
    "제주특별자치도 서귀포": (33.2530, 126.5618),
    "경상남도 남해": (34.8370, 127.8920),
    "경상남도 거제": (34.8800, 128.6210),
    "부산광역시": (35.1796, 129.0756)
}

# 5. 지도 생성
m = folium.Map(location=[34.8, 127.8], zoom_start=7)

for region in top5_regions:
    if region in region_coords:
        lat, lon = region_coords[region]
        avg_precip = region_means[region]
        folium.CircleMarker(
            location=(lat, lon),
            radius=avg_precip / 50,  # 수치에 따라 원 크기 조정
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.5,
            popup=f"{region}: {avg_precip:.1f} mm"
        ).add_to(m)
    else:
        st.warning(f"⚠️ '{region}'의 좌표 정보가 없습니다.")

# 6. 지도 표시
st.subheader("🗺️ 평균 강수량 상위 5개 지역 (지도 표시)")
st_folium(m, width=800, height=600)

# 7. 데이터프레임 출력
st.subheader("📄 지역별 평균 강수량")
df_result = pd.DataFrame({"평균 강수량 (mm)": region_means})
st.dataframe(df_result)

# 8. 안내
st.caption("※ 강수량 단위는 mm입니다. 마커 크기는 평균 강수량에 비례하며 반투명하게 표시됩니다.")
