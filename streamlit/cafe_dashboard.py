import streamlit as st
import pandas as pd
import numpy as np
import time

# Streamlit 페이지 설정
st.set_page_config(
    page_title="Little Star 카페 매출 대시보드", page_icon="☕", layout="wide"
)

# 제목 표시
st.title("☕ Little Star 카페 매출 대시보드")

# Magic 문법과 write, text element utilities 사용 예시
"""
# ✨ Little Star Cafe 4월 매출 분석
Welcome to the interactive dashboard for our beloved Little Star Cafe!
Here you can explore the daily sales, edit them, and see the impact instantly.
"""

st.header("📌 매출 데이터 편집 및 조회")
st.caption("Edit, add, or delete sales data easily below.")

# 샘플 데이터 생성 및 세션에 저장
np.random.seed(42)
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        {
            "날짜": pd.date_range(start="2025-04-01", periods=30),
            "매출액(천원)": np.random.randint(100, 500, size=30),
        }
    )

data = st.session_state.data

# 데이터 편집 기능 추가
with st.expander("🛠️ 데이터 추가/수정/삭제"):
    with st.form("edit_form"):
        option = st.radio("작업 선택", ("추가", "수정", "삭제"))
        date_input = st.date_input("날짜 입력", pd.to_datetime("2025-04-01"))
        sales_input = st.number_input(
            "매출액 입력 (천원)", min_value=0, max_value=1000, value=100
        )
        submit_button = st.form_submit_button("적용하기")

        if submit_button:
            # 입력받은 날짜를 pandas datetime64로 변환
            date_input = pd.to_datetime(date_input)

            if option == "추가":
                new_row = pd.DataFrame(
                    {"날짜": [date_input], "매출액(천원)": [sales_input]}
                )
                st.session_state.data = pd.concat(
                    [st.session_state.data, new_row], ignore_index=True
                )
                st.success("✅ 데이터가 추가되었습니다!")
            elif option == "수정":
                idx = st.session_state.data[
                    st.session_state.data["날짜"] == date_input
                ].index
                if not idx.empty:
                    st.session_state.data.loc[idx, "매출액(천원)"] = sales_input
                    st.success("✅ 데이터가 수정되었습니다!")
                else:
                    st.error("❌ 해당 날짜의 데이터가 없습니다.")
            elif option == "삭제":
                idx = st.session_state.data[
                    st.session_state.data["날짜"] == date_input
                ].index
                if not idx.empty:
                    st.session_state.data = st.session_state.data.drop(idx).reset_index(
                        drop=True
                    )
                    st.success("✅ 데이터가 삭제되었습니다!")
                else:
                    st.error("❌ 해당 날짜의 데이터가 없습니다.")

            # 날짜 타입 강제 변환 (문제 해결)
            st.session_state.data["날짜"] = pd.to_datetime(
                st.session_state.data["날짜"]
            )

# 데이터 출력
st.subheader("📅 현재 매출 데이터")
st.dataframe(st.session_state.data)

# 매출액 라인 차트
st.subheader("📈 매출액 추이")
st.line_chart(st.session_state.data.set_index("날짜"))

# 매출액 바 차트
st.subheader("📊 매출액 비교")
st.bar_chart(st.session_state.data.set_index("날짜"))

# 진행 상황 시뮬레이션
st.subheader("⏳ 데이터 처리 중...")
progress_bar = st.progress(0)
status_text = st.empty()

for i in range(100):
    status_text.text(f"진행률: {i+1}%")
    progress_bar.progress(i + 1)
    time.sleep(0.02)

st.success("✅ 데이터 처리 완료!")

# 요약 카드 추가
st.markdown("---")
col1, col2, col3 = st.columns(3)
col1.metric("📅 데이터 수", f"{len(st.session_state.data)} 일")
col2.metric(
    "📈 최고 매출액(천원)", f"{st.session_state.data['매출액(천원)'].max()} 천원"
)
col3.metric(
    "📉 최저 매출액(천원)", f"{st.session_state.data['매출액(천원)'].min()} 천원"
)

# Footer
st.markdown("---")
st.caption("Made by LJJ")
