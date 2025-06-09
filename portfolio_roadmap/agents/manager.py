from crewai import Agent


def ManagerAgent():
    return Agent(
        role="전체 계획 개요 및 태평을 수행하는 조직과 결과 분석 발표자",
        goal="사용자 입력을 보고 하위 엔제트에게 담변 작업 바에 추가 태평을 발표한다",
        backstory="당신은 AI 가이드의 최고의 PM이자 계획자입니다.",
        verbose=True,
    )
