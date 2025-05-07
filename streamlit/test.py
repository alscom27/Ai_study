import streamlit as st

st.title("안녕하세요")
st.write("반갑습니다. 스트림릿입니다.")

if "count" not in st.session_state:
    st.session_state.count = 0

if st.button("안녕"):
    st.session_state.count += 1

st.title(st.session_state.count)
