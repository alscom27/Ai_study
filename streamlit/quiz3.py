# quiz 3
import streamlit as st
import numpy as np
import time

st.title("숫자 맞추기")

if "random" not in st.session_state:
    st.session_state.random = np.random.randint(1, 101)

if "stage" not in st.session_state:
    st.session_state.stage = 0


if st.session_state.stage == 0:
    length = len(str(st.session_state.random))

    st.write(f"{'*'*length} 숫자를 맞춰보세요.")
    user_input = st.number_input(
        "1~100 숫자를 입력해주세요.", min_value=0, max_value=100, step=1
    )

    if st.button("정답 제출"):
        if st.session_state.random == user_input:
            st.write("정답입니다!")

            if st.button("다시하기"):
                st.session_state.stage = 1

        elif st.session_state.random > user_input:
            st.warning("입력하신 숫자 보다 높아요")
        else:
            st.info("입력하신 숫자 보다 낮아요.")

if st.session_state.stage == 1:
    with st.spinner("숫자 섞는중..."):
        st.session_state.random = np.random.randint(1, 101)
        time.sleep(3)
        st.session_state.stage = 0
        st.rerun()
