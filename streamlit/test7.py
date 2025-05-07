import streamlit as st
import numpy as np
import pandas as pd

# -------------------------------
# 스토리텔링
# -------------------------------
"""
# 🌐 웹사이트 방문자 수 대시보드

이 페이지는 간단한 웹사이트 방문자 수를 실시간으로 모니터링하는 예시입니다.

- Write & Magic 기능을 활용해 텍스트를 자연스럽게 작성하고,
- Text elements(Utilities)로 제목, 부제목, 구분선 등을 구성하고,
- Data elements를 활용해 메트릭(metric)과 표(dataframe)를 표현합니다.

**목표:** 초보자도 쉽게 이해하고 따라할 수 있는 대시보드 실습!
"""

# -------------------------------
# 기본 설정 및 데이터 생성
# -------------------------------

# 페이지 제목
st.title("🌐 웹사이트 방문자 수 대시보드")

# 방문자 수 데이터 생성
np.random.seed(42)
today_visitors = np.random.randint(500, 1500)
yesterday_visitors = np.random.randint(500, 1500)
change = today_visitors - yesterday_visitors

# 최근 일주일 방문자 수 데이터
weekly_data = pd.DataFrame(
    {
        "날짜": pd.date_range(end=pd.Timestamp.today(), periods=7),
        "방문자 수": np.random.randint(500, 1500, size=7),
    }
)

# -------------------------------
# 데이터 표시
# -------------------------------

# 오늘 방문자 수 메트릭
st.subheader("📊 오늘의 방문자 수")
st.metric("방문자 수", f"{today_visitors}명", f"{change:+}명")

# 최근 일주일 방문자 수 테이블
st.subheader("🗓️ 최근 일주일 방문자 수")
st.dataframe(weekly_data, use_container_width=True)

# -------------------------------
# 부가 설명
# -------------------------------

st.info(
    "방문자 수는 임의로 생성된 데이터입니다. 실제 서비스에서는 서버에서 받아온 데이터를 연결합니다."
)

# Footer
st.markdown("---")
st.caption("Made by LJJ")
