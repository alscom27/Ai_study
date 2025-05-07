import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# 스토리텔링
# -------------------------------
"""
# 🍽️ 하루 식사 칼로리 추적 대시보드

이 앱은 사용자가 선택한 하루 세 끼(아침, 점심, 저녁)에 따른 총 섭취 칼로리를 계산하고
차트로 시각화하는 간단한 식단 관리 도구입니다.

- Write & Magic으로 소개와 설명을 작성하고
- Text elements로 구조를 나누고 시각적 가독성을 높이며
- Input 위젯으로 사용자 입력을 받고
- Data elements + 차트 elements로 결과를 출력합니다.

**목표:** 식단 기록 대시보드 실습을 통해 Streamlit UI 요소 익히기
"""

# -------------------------------
# 제목 및 설명
# -------------------------------

st.title("🍽️ 하루 식사 칼로리 추적기")
st.write(
    "간단하게 아침, 점심, 저녁에 먹은 음식의 칼로리를 입력하고 하루 총 칼로리를 확인하세요."
)

# -------------------------------
# 사용자 입력 (input widgets)
# -------------------------------

st.subheader("🍳 식사별 칼로리 입력")
breakfast = st.number_input(
    "아침 (kcal)", min_value=0, max_value=2000, value=400, step=50
)
lunch = st.number_input("점심 (kcal)", min_value=0, max_value=2000, value=600, step=50)
dinner = st.number_input("저녁 (kcal)", min_value=0, max_value=2000, value=500, step=50)

# -------------------------------
# 결과 요약 및 시각화
# -------------------------------

total = breakfast + lunch + dinner
change = total - 2000

st.subheader("📊 하루 요약")
st.metric("총 섭취 칼로리", f"{total} kcal", f"{change:+} kcal")

# 바 차트 데이터 (인덱스를 명시적으로 지정해서 순서 유지)
chart_data = pd.DataFrame(
    {"칼로리": [breakfast, lunch, dinner]}, index=["아침", "점심", "저녁"]
)

st.subheader("🥗 식사별 칼로리 분포")
st.bar_chart(chart_data)

# -------------------------------
# 마무리 설명
# -------------------------------

st.info("일일 권장 섭취량은 평균 2000kcal입니다. 목표에 따라 값을 조절하세요.")

st.markdown("---")
st.caption("Made by LJJ")
