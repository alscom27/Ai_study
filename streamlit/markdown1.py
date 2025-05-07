import streamlit as st

st.markdown("# 고양이가 코딩을 할까요? :cat: ")
st.markdown("## 고양이가 코딩을 할까요? :cat: ")
st.markdown("### 고양이가 코딩을 할까요? :cat: ")
st.markdown("#### 고양이가 코딩을 할까요? :cat: ")
st.markdown("##### 고양이가 코딩을 할까요? :cat: ")
st.markdown("###### 고양이가 코딩을 할까요? :cat: ")


st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(":red[빨간 텍스트] :blue[파란 텍스트] :green[초록 텍스트]")
st.markdown(":blue-background[파란 배경 강조 텍스트]")
st.markdown(":orange-background[주황 배경 강조 텍스트]")
st.markdown("이모지 테스트 :rocket: :smile: :tulip: :fire: ")
st.markdown("수식 예시 : $\\squrt{x^2+y^2}$")

st.markdown(
    """이 문장은 줄바꿈 합니다. \n
이 줄은 아래로 내려옵니다."""
)
st.markdown(
    "이 문장은 줄바꿈합니다. <br> 이 줄은 아래로 내려옵니다.", unsafe_allow_html=True
)

st.markdown("### Soft Return 예시 (줄 끝에 공백 2칸)")
st.markdown("이 줄은 줄 끝에 공백 두 칸이 있습니다.  \n다음 줄로 내려옵니다.")
st.markdown("### Soft Return 예시 (역슬래시 n)")
st.markdown("이 줄은 역슬래시 n 사용 \n 줄바꿈이 적용됩니다.")
st.markdown("### Hard Return 예시 (문단 바꿈)")
st.markdown(
    """
문단1입니다.

문단2입니다. 완전히 다른 문단으로 처리됩니다.
"""
)
