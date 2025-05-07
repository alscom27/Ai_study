import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import datetime

# 한글 깨짐 방지용 폰트 설정
matplotlib.rcParams["font.family"] = "Malgun Gothic"  # Windows 기준
matplotlib.rcParams["axes.unicode_minus"] = False

# ---------------------------
"""
# 🧠 하루 집중도 자가 진단 대시보드
"""

# ---------------------------
st.sidebar.header("📝 오늘의 집중력 기록")
with st.sidebar.form("focus_form"):
    username = st.text_input("이름을 입력하세요")
    date = st.date_input("날짜", value=datetime.date.today())
    focus_score = st.slider("오늘의 집중 점수 (0~100)", 0, 100, 70)
    distractions = st.multiselect(
        "집중을 방해한 요소", ["스마트폰", "소음", "피곤함", "다른 일"]
    )
    note = st.text_area("추가 메모")
    submitted = st.form_submit_button("기록하기")

# ---------------------------
st.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Brain_icon.svg/1024px-Brain_icon.svg.png",
    width=100,
)

# ---------------------------
if submitted:
    st.success("기록이 저장되었습니다!")

    with st.container():
        st.header("📋 오늘의 집중 기록 요약")

        # layout row
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("👤 사용자 정보")
            st.write(f"**이름**: {username}")
            st.write(f"**날짜**: {date}")

        with col2:
            st.subheader("📈 집중도")
            st.metric("집중 점수", f"{focus_score}/100")

        st.subheader("⚠️ 방해 요소")
        st.write(", ".join(distractions) if distractions else "없음")

        st.subheader("🗒️ 메모")
        st.write(note if note else "작성된 메모 없음")

        # 차트 요소
        st.subheader("📉 점수 위치 시각화")
        fig, ax = plt.subplots()
        ax.barh(["오늘의 집중 점수"], [focus_score], color="skyblue")
        ax.set_xlim(0, 100)
        st.pyplot(fig)

# Footer
st.markdown("---")
