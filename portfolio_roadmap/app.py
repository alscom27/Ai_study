import streamlit as st
from crew_main import run_crew
from utils.formatter import format_markdown_output

st.title("🚀 CrewAI 기본 직무 가이드")

with st.form("crew_form"):
    job = st.selectbox("직무 선택", ["백엔드 개발자", "프론트엔드 개발자", "AI 개발자"])
    skill = st.text_area("현재 기술/수준", "ex) Pandas, Python 기초")
    duration = st.slider("학습 기간 (개월)", 1, 12, 6)
    submitted = st.form_submit_button("계획 만들기")

if submitted:
    with st.spinner("계획 생성 중..."):
        user_input = {"job": job, "skill": skill, "duration": duration}
        result = run_crew(user_input)
        st.markdown(format_markdown_output(result))
