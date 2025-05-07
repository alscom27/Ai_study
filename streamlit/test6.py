import streamlit as st

st.markdown("# 📌 제목1")
st.markdown("## ✨ 제목2")
st.markdown("**굵은 텍스트** 와 *기울임 텍스트* 를 같이 써봅시다.")
st.markdown("[구글로 이동](https://google.com)")
st.markdown("### 순서 없는 리스트")
st.markdown(
    """
- 사과
- 바나나
- 체리
"""
)
st.markdown("### 순서 있는 리스트")
st.markdown(
    """
1. 첫 번째
2. 두 번째
3. 세 번째
"""
)
st.markdown("> 이건 인용문입니다.")
st.markdown("### 코드 블록")
st.markdown(
    """
```
def say_hello():
 print("Hello Streamlit!")
```
"""
)
### 예시 2: `st.code()` 사용
st.code(
    """
def greet():
 print("Hi Streamlit!")
"""
)
st.markdown("`print()` 함수는 출력을 위한 Python 함수입니다.")
