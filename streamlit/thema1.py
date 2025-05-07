import streamlit as st

st.title("streamlit 기본 웹 앱")

name = st.text_input("이름을 입력하세요")

if st.button("인사하기"):
    st.write(f"안녕하세요, {name}님!")

age = st.slider("나이를 선택하세요:", 0, 100, 50)
st.write(f"{name}님의 나이는 {age}입니다.")
