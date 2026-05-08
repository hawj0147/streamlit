import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df_a = pd.read_json('heart_failure_a.json')
df_b = pd.read_json('heart_failure_b.json')

df = pd.merge(df_a, df_b, on='person_id', how='inner')
dropped_count = len(df_a) - len(df) + len(df_b) - len(df)

st.subheader("1. 데이터 병합 결과")
st.write(f"병합된 데이터 행 수: {len(df)}개")
st.write(f"삭제된 데이터 개수: {dropped_count}개")

# 4. 시각화 (Jointplot)
st.subheader("2. 박출계수와 나이의 상관관계 (Jointplot)")

# seaborn의 jointplot을 사용하여 시각화
grid = sns.jointplot(data=df, x='ejection_fraction', y='age', hue='DEATH_EVENT')

# Streamlit에 그래프 표시
st.pyplot(grid.fig)

# 5. 데이터 표 확인 (선택사항)
if st.checkbox('병합된 데이터 보기'):
    st.dataframe(df)

st.divider()
st.subheader("3. 사망 여부에 따른 혈소판 수치 (흡연 여부 선택)")

smoking_option = st.radio(
    "흡연 여부 표시 방식 선택:",
    ('전체 데이터 보기', '흡연 여부별로 나눠보기 (Split)')
)

fig, ax = plt.subplots(figsize=(10, 6))

if smoking_option == '전체 데이터 보기':
    sns.violinplot(data=df, x='DEATH_EVENT', y='platelets', ax=ax)
    ax.set_title("Platelets vs Death Event (Total)")
else:
    sns.violinplot(data=df, x='DEATH_EVENT', y='platelets', hue='smoking', split=True)
    ax.set_title("Platelets vs Death Event (Split by Smoking)")

st.pyplot(fig)

st.divider()
st.subheader("4. 심박출률(Ejection Fraction) 범위에 따른 생존 기간 분석")

# 1. 슬라이더로 심박출률(ejection_fraction) 범위 선택
# 데이터의 최소값과 최대값을 가져와 슬라이더의 범위를 설정합니다.
min_ef = int(df['ejection_fraction'].min())
max_ef = int(df['ejection_fraction'].max())

# 슬라이더 생성 (최소값, 최대값, (초기 선택 범위))
selected_ef = st.slider(
    '심박출률(ejection_fraction) 범위를 선택하세요',
    min_ef, max_ef, (min_ef, max_ef)
)

# 2. 선택된 범위로 데이터 필터링
# selected_ef[0]은 시작값, selected_ef[1]은 끝값입니다.
filtered_df = df[
    (df['ejection_fraction'] >= selected_ef[0]) & 
    (df['ejection_fraction'] <= selected_ef[1])
]

# 3. 히스토그램 시각화
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(data=filtered_df, x='time', bins=20, hue='DEATH_EVENT', ax=ax, kde=True)
ax.set_title(f"Time Distribution (EF: {selected_ef[0]}% - {selected_ef[1]}%)")

# 4. 결과 출력
st.write(f"현재 선택된 범위의 데이터 개수: {len(filtered_df)}개")
st.pyplot(fig)