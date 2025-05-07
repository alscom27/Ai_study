import streamlit as st
import datetime
import pandas as pd

st.title("📊 일일 운동 루틴 기록")

"""
이 예시는 Streamlit의 다양한 Input 위젯을 활용하여
사용자가 매일 수행한 운동 루틴을 기록하고 요약할 수 있도록 구성된 실습입니다.

운동 강도, 시간, 즐거움 정도, 종류 등을 기록하고 요약합니다.
"""

st.header("🏃‍♂️ 운동 기록 입력")
today = st.date_input("운동한 날짜를 선택하세요", value=datetime.date.today())
exercise_type = st.selectbox(
    "운동 종류를 선택하세요", ["헬스", "달리기", "요가", "자전거", "수영", "기타"]
)
duration = st.slider("운동 시간 (분)", min_value=10, max_value=180, value=60, step=10)
intensity = st.radio("운동 강도는 어땠나요?", ["약함", "보통", "강함"])
fun_level = st.slider("운동이 얼마나 즐거웠나요? (1~10)", 1, 10, 7)
notes = st.text_area("기타 메모를 자유롭게 입력하세요")
submit = st.button("✅ 오늘 운동 기록 저장하기")

if submit:
    st.success("운동 기록이 저장되었습니다!")

    st.header("📋 오늘의 운동 요약")
    st.markdown(f"**날짜**: {today}")
    st.markdown(f"**운동 종류**: {exercise_type}")
    st.markdown(f"**운동 시간**: {duration}분")
    st.markdown(f"**운동 강도**: {intensity}")
    st.markdown(f"**즐거움 점수**: {fun_level}/10")
    st.markdown(f"**메모**: {notes if notes else '없음'}")

st.markdown("---")
st.caption("Made by LJJ - 운동 루틴 기록 앱")
