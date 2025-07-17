import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 좌표 데이터 (예시) — 실제 행정구역명과 좌표를 맞게 수정하세요.
# 예) {'서울특별시': [37.5665, 126.9780], ...}
location_dict = {
    '서울특별시': [37.5665, 126.9780],
    '부산광역시': [35.1796, 129.0756],
    '대구광역시': [35.8722, 128.6025],
    '인천광역시': [37.4563, 126.7052],
    '광주광역시': [35.1595, 126.8526],
    # 필요에 따라 추가
}

st.title("2025년 5월 기준 연령별 인구 현황 - 지도 표시")

df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding='euc-kr')

# 데이터 전처리
df['총인구수'] = df['2025년05월_계_총인구수'].str.replace(',', '').astype(int)
age_columns = [col for col in df.columns if col.startswith('2025년05월_계_') and ('세' in col or '100세 이상' in col)]
new_columns = []
for col in age_columns:
    if '100세 이상' in col:
        new_columns.append('100세 이상')
    else:
        new_columns.append(col.replace('2025년05월_계_', '').replace('세', '') + '세')
df_age = df[['행정구역', '총인구수'] + age_columns].copy()
df_age.columns = ['행정구역', '총인구수'] + new_columns

# 상위 5개 행정구역 추출
top5_df = df_age.sort_values(by='총인구수', ascending=False).head(5)

# folium 지도 생성 (대한민국 중심 좌표, 줌레벨 7)
m = folium.Map(location=[36.5, 127.8], zoom_start=7)

# 마커 추가 (반투명 원형 마커)
for _, row in top5_df.iterrows():
    region = row['행정구역']
    if region in location_dict:
        lat, lon = location_dict[region]
        radius = row['총인구수'] / 10000  # 인구수에 비례하는 반경 (적당히 조절)
        folium.CircleMarker(
            location=[lat, lon],
            radius=radius,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.4,
            popup=f"{region}\n총인구수: {row['총인구수']:,}"
        ).add_to(m)

st.subheader("📍 인구 상위 5개 행정구역 위치")

# Streamlit에 folium 지도 표시
st_data = st_folium(m, width=700, height=500)
