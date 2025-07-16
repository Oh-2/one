import streamlit as st
import pandas as pd

st.set_page_config(page_title="연령별 인구 현황 분석", layout="wide")

st.title("📊 2025년 5월 기준 연령별 인구 현황 분석")
st.markdown("업로드한 인구 통계 데이터를 바탕으로 **상위 5개 행정구역의 연령별 인구 현황**을 시각화합니다.")

uploaded_file = st.file_uploader("CSV 파일 업로드 (EUC-KR 인코딩)", type="csv")

if uploaded_file is not None:
    # CSV 파일 읽기 (EUC-KR 인코딩)
    df = pd.read_csv(uploaded_file, encoding='euc-kr')
    df.columns = df.columns.str.strip()  # 열 이름 공백 제거

    # 필요한 열 추출
    target_cols = ['행정구역', '2025년05월_계_총인구수'] + [
        col for col in df.columns if col.startswith('2025년05월_계_') and '세' in col
    ]
    df = df[target_cols]

    # 총인구수 컬럼 숫자로 변환
    df['총인구수'] = df['2025년05월_계_총인구수'].str.replace(',', '').astype(int)

    # 연령별 열 이름 정리 ('2025년05월_계_0세' → '0', '100세 이상' → '100')
    new_columns = ['행정구역', '2025년05월_계_총인구수', '총인구수']
    age_columns = []
    for col in df.columns[2:-1]:  # 연령별 열만
        age_label = col.replace('2025년05월_계_', '').replace('세', '').replace(' 이상', '')
        age_columns.append(int(age_label) if age_label.isdigit() else age_label)
    df.columns = new_columns + age_columns

    # 상위 5개 행정구역 추출
    top5 = df.sort_values(by='총인구수', ascending=False).head(5)

    st.subheader("📋 원본 데이터 (상위 5개 행정구역)")
    st.dataframe(top5[['행정구역', '총인구수'] + age_columns], use_container_width=True)

    # 연령별 인구 선 그래프
    st.subheader("📈 연령별 인구 분포 (선 그래프)")

    for idx, row in top5.iterrows():
        age_data = pd.DataFrame({
            '연령': age_columns,
            '인구수': [int(str(row[age]).replace(',', '')) for age in age_columns]
        }).set_index('연령')
        st.markdown(f"**{row['행정구역']}**")
        st.line_chart(age_data)

else:
    st.info("왼쪽 사이드바 또는 위의 파일 선택 버튼을 통해 CSV 파일을 업로드해 주세요.")
