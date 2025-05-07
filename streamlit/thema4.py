import streamlit as st
import pandas as pd
from datetime import datetime as dt
import datetime

# 1. 텍스트입력(여행지)
title = st.text_input(
    label="가고 싶은 여행지가 있나요?", placeholder="예: 몰디브, 도쿄, 아이슬란드..."
)

if title:
    st.write(f"당신이 선택한 여행지 : :violet[{title}]")

# 2. 숫자 입력(나이)
age = st.number_input(label="나이를 입력해주세요.", min_value=10, max_value=100, step=1)
st.write("당신이 입력한 나이는 :", age)

# 3. 라디오 버튼 (커피취향)
coffee = st.radio("어떤 커피를 좋아하시나요>", ("아메리카노", "라떼", "선택 안 함"))

if coffee == "아메리카노":
    st.write("시원한 :blue[아메리카노] 준비 중...")
elif coffee == "라떼":
    st.write("부드러운 :orange[라떼] 추천드려요!")
else:
    st.write("나중에 원하실 때 말씀해주세요. :releved:")

# 4. 셀렉트 박스 (영화 장르)
genre = st.selectbox(
    "좋아하는 영화 장르는 무엇인가요?",
    ["액션", "코미디", "다큐멘터리", "선택 안 함"],
    index=3,
)
if genre != "선택 안 함":
    st.write(f"당신은 :gree[{genre}] 장르를 좋아하시는군요!")

# 5. 멀티셀렉트 (과일 선택)
fruits = st.multiselect(
    "좋아하는 과일을 모두 골라주세요!",
    ["딸기", "수박", "복숭아", "포도"],
    default=["딸기", "포도"],
)

st.write(f"🍇선택하신 과일: :violet[{fruits}]")
# ========================================
# [6] 숫자 범위 슬라이더
# ========================================
price_range = st.slider(
    "💰 원하는 가격대 (만원)", min_value=0.0, max_value=100.0, value=(30.0, 70.0)
)
st.write(f"선택한 가격 범위: {price_range[0]}만원 ~ {price_range[1]}만원")

# ========================================
# [7] 날짜/시간 슬라이더
# ========================================
start_time = st.slider(
    "📅약속 가능한 시간 선택",
    min_value=dt(2025, 3, 25, 9, 0),
    max_value=dt(2025, 3, 25, 18, 0),
    value=dt(2025, 3, 25, 13, 0),
    step=datetime.timedelta(minutes=30),
    format="HH:mm",
)
st.write("선택하신 시간:", start_time.strftime("%H:%M"))
# ========================================
# [8] 체크박스 (동의)
# ========================================
agree = st.checkbox("✅ 개인정보 제공에 동의합니다")
if agree:
    st.info("감사합니다! 데이터를 보여드릴게요.")
