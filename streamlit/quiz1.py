import streamlit as st
import time

if "stage" not in st.session_state:
    st.session_state.stage = 0

st.header("프로필")

# quiz1
name = st.text_input("이름을 입력하세요.", placeholder="홍길동")
age = st.number_input("나이를 입력하세요.", placeholder=30, min_value=0, step=1)

if st.button("제출"):

    if name == "":
        st.warning("이름을 입력해주세요.")
    elif age == 0:
        st.warning("나이를 입력해주세요.")

    if name != "" and age != 0:
        login = st.write(f"{name} 님은", end=" ")
        if age >= 20:
            st.write("성인입니다.")
        else:
            st.write("미자입니다.")
    st.session_state.stage = 1
    time.sleep(2)

# quiz2
if st.session_state.stage == 1:
    height = st.slider("키(cm)", 100, 170, 300)
    weight = st.slider("몸무게(kg)", 0, 70, 200)

    bmi = weight / ((height / 100) ** 2)

    if st.button("검사"):
        st.title(f"{name}님의 BMI는 {bmi:.2f}입니다.")
