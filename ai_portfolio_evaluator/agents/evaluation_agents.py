from crewai import Agent
from tools.pdf_tools import get_pdf_search_tool


def load_agents(pdf_path: str, job_role: str = "백엔드 개발자"):
    """포트폴리오 평가에 사용할 CrewAI 에이전트들을 반환"""

    pdf_tool = get_pdf_search_tool(pdf_path)

    # 1. 직무 전문가
    job_expert = Agent(
        role=f"{job_role} 전문가",
        goal=(
            f"{job_role} 직무에 적합한지를 평가한다. "
            "PDFSearchTool을 사용할 때는 반드시 다음 형식으로 query를 전달해야 한다:\n"
            '{"query": "검색하고 싶은 내용"}'
        ),
        backstory=f"너는 10년차 {job_role} 면접관이자 실무 전문가야. 실무 중심으로 문서를 평가해.",
        tools=[pdf_tool],
        verbose=True,
    )

    # 2. 표현력 면접관
    interviewer = Agent(
        role="인성 및 표현력 평가 면접관",
        goal=(
            "문서의 구성력, 표현력, 논리성 등을 평가한다. "
            'PDFSearchTool을 사용할 때는 반드시 문자열 query를 JSON 형식으로 넘겨야 한다. 예: {"query": "논리력"}'
        ),
        backstory="너는 사람의 사고력과 설득력을 중점적으로 보는 면접관이야.",
        tools=[pdf_tool],
        verbose=True,
    )

    # 3. 피드백 코치
    feedback_coach = Agent(
        role="포트폴리오&리포트 피드백 코치",
        goal=(
            "강점, 개선 사항, 수정 제안을 도출한다. "
            'PDFSearchTool을 사용할 때는 반드시 query는 문자열이어야 하며, 예: {"query": "강점"}'
        ),
        backstory="문서 개선에 탁월한 전문가로, 구체적인 피드백을 줄 수 있다.",
        tools=[pdf_tool],
        verbose=True,
    )

    return [job_expert, interviewer, feedback_coach]
