from dotenv import load_dotenv
import os
from crewai import Crew, Task
from agents.manager import ManagerAgent
from agents.skill_planner import SkillPlannerAgent
from agents.project_agent import ProjectAgent
from agents.checkup_agent import CheckupAgent

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


def run_crew(user_input):
    manager = ManagerAgent()
    skill = SkillPlannerAgent()
    project = ProjectAgent()
    checkup = CheckupAgent()

    task = Task(
        description=f"""
        다음 사용자 정보를 기반으로 전체 학습 및 포트폴리오 로드맵을 구성하고,
        하위 에이전트들에게 업무를 분배하여 종합된 결과를 도출하세요:

        🔹 직무: {user_input['job']}
        🔹 현재 기술: {user_input['skill']}
        🔹 목표 기간: {user_input['duration']}개월
        """,
        expected_output="기초→중급→실전 순서의 학습 경로, 2~3개의 포트폴리오 예시, 중간 점검 피드백이 포함된 마크다운 결과",
        agent=manager,
    )

    crew = Crew(agents=[manager, skill, project, checkup], tasks=[task])

    result = crew.kickoff()  # 👈 여기가 핵심! run() ❌ → kickoff() ✅
    return result
