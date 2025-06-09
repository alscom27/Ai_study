# 파일명 예시: crew_planner.py

import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain.chat_models import ChatOpenAI

# ====================
# 1. 🔐 API 키 로딩 (.env)
# ====================
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

if not openai_key:
    st.error("❌ .env에 OPENAI_API_KEY가 없습니다.")
    st.stop()
else:
    os.environ["OPENAI_API_KEY"] = openai_key

# ====================
# 2. 🎨 Streamlit UI
# ====================
st.set_page_config(page_title="AI 진로 코치 & 학습 챌린지")
st.title("🎯 진로 설계 + 학습 챌린지 생성기 (CrewAI 기반)")

goal = st.text_input("최종 목표를 입력하세요 (예: AI 개발자)", value="AI 개발자")
level = st.selectbox("현재 수준을 선택하세요", ["입문", "중급", "고급"])
duration = st.slider("목표 기간 (개월)", min_value=1, max_value=12, value=6)
weekly_time = st.slider(
    "주간 학습 가능 시간 (시간)", min_value=1, max_value=40, value=5
)

if st.button("🚀 학습 계획 생성하기"):

    # ====================
    # 3. 🤖 LLM 정의 (GPT-4)
    # ====================
    llm = ChatOpenAI(model="gpt-4", temperature=0.5)

    # ====================
    # 4. 👤 Agent 정의
    # ====================
    # 4-1) Manager Agent: “계층 구조대로 작업을 분배하고 결과를 종합하여 보고서를 작성하라”
    manager = Agent(
        role="프로젝트 매니저",
        goal=(
            "1) 진로 분석가, 전략 설계자, 단기 실행 코치, 챌린지 마스터에게 각각 "
            "단계별 업무를 분배하라.\n"
            "2) 각 Agent가 만들어 준 출력을 계층 구조대로 정리하여 최종 보고서를 작성하라.\n"
            "모든 결과물은 한국어로 작성한다."
        ),
        backstory="5년 경력의 시니어 PM으로 복잡한 협업 상황을 잘 통제한다.",
        verbose=True,
        llm=ChatOpenAI(model="gpt-4", temperature=0.4),
    )

    # 4-2) 각 Agent 정의
    goal_agent = Agent(
        role="진로 분석가",
        goal="사용자의 최종 목표(예: AI 개발자)를 분석하여, 현재 수준을 고려해 3~5개의 핵심 역량을 도출한다.",
        backstory="직업 분석 전문가로 수많은 커리어 설계를 도와온 경험이 있다.",
        verbose=True,
        llm=llm,
    )

    mid_agent = Agent(
        role="전략 설계자",
        goal="진로 분석가가 도출한 핵심 역량을 바탕으로, 중기(3~6개월) 학습 로드맵을 설계한다.",
        backstory="직무 기반 학습 로드맵을 잘게 쪼개 설계하는 전문가이다.",
        verbose=True,
        llm=llm,
    )

    short_agent = Agent(
        role="단기 실행 코치",
        goal="전략 설계자가 만든 중기 로드맵을 주차별 실행 계획으로 세부 분해한다.",
        backstory="구체적인 실천 단위로 쪼개어 실행을 도와주는 전문가이다.",
        verbose=True,
        llm=llm,
    )

    challenge_agent = Agent(
        role="학습 챌린지 마스터",
        goal="단기 실행 계획을 기반으로, 각 주차별로 수행할 ‘도전 과제(챌린지)’를 설계한다.",
        backstory="지루한 학습을 재미있는 챌린지로 바꿔주는 데 특화된 AI이다.",
        verbose=True,
        llm=llm,
    )

    # ====================
    # 5. 🧩 Task 정의 (expected_output 포함)
    # ====================
    task1 = Task(
        agent=goal_agent,
        description=(
            f"1) 최종 목표: '{goal}' (현재 수준: {level})를 기반으로\n"
            "2) AI 개발자로서 필수적인 핵심 역량 3~5개를 도출하세요."
        ),
        expected_output="핵심 역량 리스트",
    )

    task2 = Task(
        agent=mid_agent,
        description=(
            "1) 진로 분석가가 제시한 핵심 역량을 입력받아,\n"
            "2) 각 역량을 강화하기 위한 중기(3~6개월) 학습 로드맵을 설계하세요.\n"
            "   - 각 모듈은 2~3단계로 나누고 간단한 설명을 덧붙이세요."
        ),
        expected_output="중기 학습 로드맵",
    )

    task3 = Task(
        agent=short_agent,
        description=(
            f"1) 전략 설계자가 만든 중기 로드맵을 바탕으로,\n"
            f"2) {duration}개월(주차 단위) 동안의 세부 실행 계획표를 작성하세요.\n"
            f"   - 주당 학습 가능 시간: {weekly_time}시간\n"
            "   - 각 주차에 해야 할 학습 항목과 예상 소요 시간을 명시하세요."
        ),
        expected_output="주차별 실행 계획표",
    )

    task4 = Task(
        agent=challenge_agent,
        description=(
            "1) 단기 실행 코치가 만든 주차별 실행 계획을 참조하여,\n"
            "2) 각 주차마다 수행할 실용적인 도전 과제(챌린지)를 설계하세요.\n"
            "   - 과제명, 설명, 난이도(입문/중급/고급), 예상 소요 시간을 포함하세요."
        ),
        expected_output="주차별 학습 챌린지 리스트",
    )

    # ====================
    # 6. 🎯 Crew 정의 및 실행
    # ====================
    crew = Crew(
        agents=[goal_agent, mid_agent, short_agent, challenge_agent],
        tasks=[task1, task2, task3, task4],
        process=Process.hierarchical,
        manager_agent=manager,  # ✅ manager_llm 대신 manager_agent 사용
        verbose=True,
    )

    # Kickoff: 각 Agent가 작업을 수행하고 Manager가 최종 요약
    crew.kickoff()

    # ====================
    # 7. ✅ Agent별 출력(계층 구조 드러내기)
    # ====================
    st.subheader("📂 Agent별 / 계층별 결과물")

    # 7-1) 진로 분석가 결과
    st.markdown("### 1️⃣ 진로 분석가 (핵심 역량 도출)")
    if task1.output:
        st.markdown(task1.output)
    else:
        st.markdown("_결과 없음_")

    # 7-2) 전략 설계자 결과
    st.markdown("### 2️⃣ 전략 설계자 (중기 학습 로드맵)")
    if task2.output:
        st.markdown(task2.output)
    else:
        st.markdown("_결과 없음_")

    # 7-3) 단기 실행 코치 결과
    st.markdown("### 3️⃣ 단기 실행 코치 (주차별 실행 계획표)")
    if task3.output:
        st.markdown(task3.output)
    else:
        st.markdown("_결과 없음_")

    # 7-4) 학습 챌린지 마스터 결과
    st.markdown("### 4️⃣ 학습 챌린지 마스터 (주차별 학습 챌린지)")
    if task4.output:
        st.markdown(task4.output)
    else:
        st.markdown("_결과 없음_")

    # ====================
    # 8. 📝 Manager 요약 (전체 계층 구조 보고서)
    # ====================
    st.subheader("📑 프로젝트 매니저 최종 보고서")
    # manager_agent가 만든 전체 요약은 crew.manager_response에 저장됩니다.
    if crew.manager_response:
        st.markdown(crew.manager_response)
    else:
        st.markdown("_Manager 보고서 없음_")
