def format_markdown_output(result_dict):
    """
    각 에이전트의 출력 결과를 마크다운 형식으로 정리합니다.
    """
    output = ""
    for agent_name, content in result_dict.items():
        output += f"### 🔹 {agent_name}\n"
        output += content.strip() + "\n\n"
    return output
