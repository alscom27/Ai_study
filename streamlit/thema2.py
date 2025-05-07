import streamlit as st

# 1. 페이지 타이틀 설정
st.title("streamlit ui 요소 데모")

st.title("고양이도 코딩을 합니다 :cat:")


# 2. 헤더와 서브헤더
st.header("헤더 영역입니다.")

st.subheader("이곳은 서브헤더입니다.")

# 3. 캡션 표시
st.caption("작성자 : streamlit 연습생 | 날짜 : 2025-04-30")

# 4. 코드 블록 출력
st.caption("아래는 Python 코드 예시입니다.")
example_code = """
def calculate_area(radius):
    pi = 3.141592
    return pi * (radius^2)
    
print(calculate_area(5))
"""
st.code(example_code, language="python")

# 5. 일반 텍스트 출력
st.text("이것은 일반 텍스트입니다. 마크다운도 스타일도 적용되지 않았습니다.")

# 6. 마크다운 문법
st.markdown(
    "streamlit은 마크다운 문법을 지원 하며, _기울임_, 굵게, `코도`도 가능합니다."
)

st.markdown("- 리스트 항목 1\n- 리스트 항목 2\n- 리스트 항목 3")

st.markdown("여기서는 :red[빨간색], :green[초록색], :blue[파란색] 텍스트를 보여줍니다.")

st.markdown("✔️ 이것은 체크표시 이모지입니다.")

# 7. 수학 수식 표현(LaTex)
st.latex(r"E = mc^2")

# 마크다운에 포함된 색상 + 수식
st.markdown("삼각함수 항등식 : :blue[$\\sin^2\\theta + \\cos^2 \\theta = 1$]")

# 어려운 수식 설명을 위한 확장 영역
with st.expander("수식 설명 보기"):
    st.markdown(
        """
                위 식은 삼각함수의 항등식 으로, 단위원 상에서 각도 0에 대한
                `사인과 코사인의 제곱의 합은 항상1`이라는 성질을 말합니다.
                다양한 수학적 증명과 물리 공식의 기본 단위로 자주 등장합니다.
                """
    )

# 8. 하단 캡션 및 크레딧
st.caption("2025 streamlit 예제 데모")
