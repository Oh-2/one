import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="시 단위 연령별 인구 분석", layout="wide")

st.title("🏙️ 시 단위 연령별 인구 현황 분석 (2025년 5월 기준)")

file_path = "202505_202505_연령별인구현황_월간.csv"

# 파일이 없을 경우 메시지 출력
if not os.path.exists(file_path):
    st.error(f"CSV 파일이 존재하지 않습니다: {file_path}")
else:
    # CSV 읽기
    df = pd.read_csv(file_path, encoding='euc-kr')
    df.columns = df.columns.str.strip()

    # 필요한 열 추출
    age_cols = [col for col in df.columns if col.startswith('2025년05월_계_') and '세' in col]
    df = df[['행정구역', '2025년05월_계_총인구수'] + age_cols]

    # 총인구수 정수형 변환
    df['총인구수'] = df['2025년05월_계_총인구수'].str.replace(',', '').astype(int)

    # 광역시/도 이름만 추출 (예: '서울특별시 중구' → '서울특별시')
    df['시도'] = df['행정구역'].str.extract(r'^([^\s]+)')

    # 시도 단위로 집계
    grouped = df.groupby('시도').sum(numeric_only=True).reset_index()

    # 열 이름 정리: '2025년05월_계_0세' → '0'
    clean_columns = ['시도', '총인구수'] + [
        col.replace('2025년05월_계_', '').replace('세', '').replace(' 이상', '') for col in age_cols
    ]
    grouped.columns = clean_columns

    # 연령 열 숫자로 변환
    age_numbers = []
    for col in clean_columns[2:]:
        try:
            age_numbers.append(int(col))
        except:
            age_numbers.append(col)
    grouped.columns = ['시도', '총인구수'] + age_numbers

    # 상위 5개 시도 선택
    top5 = grouped.sort_values(by='총인구수', ascending=False).head(5)

    st.subheader("📋 상위 5개 시도별 총인구수")
    st.dataframe(top5[['시도', '총인구수']], use_container_width=True)

    st.subheader("📈 시도별 연령 인구 분포 (선 그래프)")

    for _, row in top5.iterrows():
        age_data = pd.DataFrame({
            '연령': age_numbers,
            '인구수': [row[age] for age in age_numbers]
        }).set_index('연령')

        st.markdown(f"### {row['시도']}")
        st.line_chart(age_data)
