import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="시 단위 연령별 인구 분석", layout="wide")

st.title("연령별 인구 현황 분석 (2025년 5월 기준)")

# CSV 파일 경로
file_path = "202505_202505_연령별인구현황_월간.csv"

if not os.path.exists(file_path):
    st.error(f"CSV 파일이 존재하지 않습니다: {file_path}")
else:
    # 1. 파일 불러오기
    df = pd.read_csv(file_path, encoding='euc-kr')
    df.columns = df.columns.str.strip()

    # 2. 필요한 열 선택
    age_cols = [col for col in df.columns if col.startswith('2025년05월_계_') and '세' in col]
    df = df[['행정구역', '2025년05월_계_총인구수'] + age_cols]

    # 3. 총인구수 숫자형으로 변환
    df['2025년05월_계_총인구수'] = df['2025년05월_계_총인구수'].str.replace(',', '').astype(int)

    # 4. 시도 이름 추출 (서울특별시 종로구 → 서울특별시)
    df['시도'] = df['행정구역'].str.extract(r'^([^\s]+)')

    # 5. 시도 단위로 집계 (총인구수 포함)
    grouped = df.groupby('시도')[['2025년05월_계_총인구수'] + age_cols].sum(numeric_only=True).reset_index()

    # 6. 열 이름 정리
    clean_columns = ['시도', '총인구수'] + [
        col.replace('2025년05월_계_', '').replace('세', '').replace(' 이상', '') for col in age_cols
    ]
    grouped.columns = clean_columns

    # 7. 연령 숫자 리스트 만들기
    age_numbers = []
    for col in clean_columns[2:]:
        try:
            age_numbers.append(int(col))
        except:
            age_numbers.append(col)

    # 8. 열 이름 최종 적용
    grouped.columns = ['시도', '총인구수'] + age_numbers

    # 9. 총인구수 기준 상위 5개 시도 추출
    top5 = grouped.sort_values(by='총인구수', ascending=False).head(5)

    # 10. 원본 표 출력
    st.subheader("📋 상위 5개 시도별 총인구수")
    st.dataframe(top5[['시도', '총인구수']], use_container_width=True)

    # 11. 그래프 출력
    st.subheader("📈 시도별 연령 인구 분포 (선 그래프)")

    for _, row in top5.iterrows():
        age_data = pd.DataFrame({
            '연령': age_numbers,
            '인구수': [row[age] for age in age_numbers]
        }).set_index('연령')

        st.markdown(f"### {row['시도']}")
        st.line_chart(age_data)
