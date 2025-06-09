# # evaluator/evaluation_engine.py

# from crewai import Task, Crew
# from agents.evaluation_agents import load_agents


# def run_evaluation(pdf_path: str, job_role: str = "백엔드 개발자") -> str:
#     """PDF를 기반으로 에이전트 평가를 실행하고 모든 결과를 종합해 문자열로 반환"""

#     # 1. 에이전트 불러오기
#     agents = load_agents(pdf_path, job_role)

#     # 2. Task 정의
#     tasks = [
#         Task(
#             description=(
#                 f"업로드된 포트폴리오가 '{job_role}' 직무에 얼마나 적합한지 평가하세요.\n"
#                 "다음 항목을 포함하세요:\n"
#                 "- 점수 (100점 만점)\n"
#                 "- 평가 근거\n"
#                 "- 최종 판단 (예: 합격 가능 / 불가능 / 보완 필요)\n\n"
#                 "PDFSearchTool을 사용할 때는 반드시 다음과 같이 입력:\n"
#                 'Action Input: {"query": "백엔드 개발"}'
#             ),
#             expected_output="점수, 평가 근거, 최종 판단",
#             agent=agents[0],
#         ),
#         Task(
#             description=(
#                 "문서의 구성력, 표현력, 전달력 등을 평가하세요.\n"
#                 "다음 항목을 포함하세요:\n"
#                 "- 구성력 점수 (100점)\n"
#                 "- 문장력 / 논리력 피드백\n"
#                 "- 수정이 필요한 부분\n\n"
#                 "PDFSearchTool 사용 예시:\n"
#                 'Action Input: {"query": "표현력"}'
#             ),
#             expected_output="구성력 점수, 문장력/논리력 평가, 수정 제안",
#             agent=agents[1],
#         ),
#         Task(
#             description=(
#                 "이 포트폴리오의 강점과 개선 포인트를 아래 형식으로 작성하세요:\n\n"
#                 "[강점 목록]\n- 예시\n[개선 사항]\n- 예시\n[수정 제안]\n- 예시\n\n"
#                 "PDFSearchTool을 사용할 때는 query는 반드시 문자열이어야 합니다.\n"
#                 'Action Input: {"query": "강점"}'
#             ),
#             expected_output="강점, 개선 사항, 수정 제안",
#             agent=agents[2],
#         ),
#     ]

#     # 3. Crew 실행
#     crew = Crew(agents=agents, tasks=tasks, verbose=True)
#     crew.kickoff()

#     # 4. 모든 결과 종합
#     results = []
#     for i, task in enumerate(tasks, start=1):
#         results.append(f"## 🧩 평가 항목 {i} - {task.agent.role}\n\n{task.output}\n")

#     return "\n---\n".join(results)


# # 디버깅용 로그
# print("✅ [evaluation_engine] run_evaluation 정의 완료")
# print("✅ globals:", list(globals().keys()))

from crewai import Task, Crew, Process
from agents.evaluation_agents import load_agents


def run_evaluation(pdf_path: str, job_role: str = "백엔드 개발자") -> str:
    """PDF를 기반으로 에이전트 평가를 실행하고 종합 결과를 문자열로 반환"""

    # 1. 에이전트 불러오기
    agents = load_agents(pdf_path, job_role)

    # 2. 각 에이전트에게 Task 정의
    tasks = [
        Task(
            description=f"""업로드된 포트폴리오가 '{job_role}' 직무에 얼마나 적합한지 평가하라.
            점수(100점 만점)와 평가 이유, 합격 가능 여부를 작성하라.""",
            expected_output="점수(100점 만점), 평가 이유, 합격 가능성 판단",
            agent=agents[0],
        ),
        Task(
            description="""문서의 구성력, 표현력, 전달력, 논리성 등을 분석하여 평가하라.
            점수와 함께 개선 포인트가 있다면 피드백도 작성하라.""",
            expected_output="표현력 점수, 논리력, 문장력 피드백, 개선 제안",
            agent=agents[1],
        ),
        Task(
            description="""앞선 두 평가 결과를 종합하여 이 포트폴리오의 강점과 약점을 분석하고
            전체적인 합격 가능성을 판단하라. 보완할 부분도 제안하라.""",
            expected_output="종합 피드백, 강점 목록, 개선 사항, 합격 여부, 최종 점수",
            agent=agents[2],
        ),
    ]

    # 3. Crew 정의 및 순차 처리 프로세스 적용
    crew = Crew(
        agents=agents,
        tasks=tasks,
        process=Process.sequential,  # ✅ 순차 처리 적용!
        verbose=True,
    )

    # 4. 실행 및 결과 수집
    final_output = crew.kickoff()
    return final_output


# 디버깅 로그 (필요 시 유지)
print("✅ [evaluation_engine] run_evaluation 정의 완료")
