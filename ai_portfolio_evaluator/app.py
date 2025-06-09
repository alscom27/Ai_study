import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from evaluator.evaluation_engine import run_evaluation
from tools.pdf_tools import save_uploaded_pdf

import evaluator.evaluation_engine as ee

print("🧪 run_evaluation 있음:", hasattr(ee, "run_evaluation"))  # True 떠야 함


st.set_page_config(page_title="AI 포트폴리오 평가관", layout="wide")

st.title("📊 AI 포트폴리오 평가관")
st.markdown("AI 전문가들이 당신의 포트폴리오를 분석하여 점수와 피드백을 제공합니다.")

# 1. 파일 업로드
uploaded_file = st.file_uploader("📁 PDF 포트폴리오 업로드", type=["pdf"])

# 2. 직무 선택
job_role = st.selectbox(
    "🔍 평가받고 싶은 직무를 선택하세요",
    [
        "",
        "백엔드 개발자",
        "프론트엔드 개발자",
        "데이터 분석가",
        "디자이너",
        "AI 연구원",
    ],
)

# 3. 평가 버튼
start = st.button("🚀 평가 시작")

if start:
    if uploaded_file and job_role:
        with st.spinner("🧠 AI 에이전트들이 평가 중입니다..."):
            # PDF 저장
            pdf_path = save_uploaded_pdf(uploaded_file)

            # CrewAI 평가 실행
            result = run_evaluation(pdf_path, job_role)

        st.success("✅ 평가 완료!")
        st.subheader("📋 평가 요약 및 피드백")
        st.markdown(result)

    elif not uploaded_file:
        st.warning("PDF 파일을 업로드해주세요.")

    elif not job_role or job_role == "":
        st.warning("직무를 선택해주세요.")
