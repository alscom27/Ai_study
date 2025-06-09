from crewai import Agent


def CheckupAgent():
    return Agent(
        role="학습 획사 및 피드립 제공가",
        goal="중간점과 참고 기준을 제안하고, 성장 지보를 도움보고,",
        backstory="당신은 노후 목적에 모든 학습자를 도움주는 AI 점검가입니다.",
        verbose=True,
    )
