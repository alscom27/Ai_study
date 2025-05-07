import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import calendar
import datetime
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import easyocr
import re


# Initialize EasyOCR
@st.cache_resource
def load_ocr_model():
    return easyocr.Reader(["ko", "en"])  # Korean + English


reader = load_ocr_model()


# OCR from image using EasyOCR
def extract_text_from_image(image):
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
    result = reader.readtext(thresh, detail=0)
    return "\n".join(result)


# 품목/금액 자동 추출 시도 (간단한 패턴 기반)
def parse_items(text):
    lines = text.split("\n")
    items = []
    for line in lines:
        match = re.match(r"(.*?)(\d{1,3}(,\d{3})*|\d+)(원|\s|$)", line)
        if match:
            item_name = match.group(1).strip()
            amount = re.findall(r"\d{1,3}(,\d{3})*|\d+", line)
            if item_name and amount:
                try:
                    value = int(amount[-1].replace(",", ""))
                    items.append((item_name, value))
                except:
                    continue
    return items


# OCR에서 총액 추출 시도
def extract_total_amount(text):
    match = re.search(r"(합계|총액|총\s*금액|매출금액).*?(\d{1,3}(,\d{3})*|\d+)", text)
    if match:
        try:
            return int(match.group(2).replace(",", ""))
        except:
            return None
    return None


# Load or initialize expense data
def load_data():
    try:
        df = pd.read_csv("expenses.csv")
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])
    except FileNotFoundError:
        df = pd.DataFrame(columns=["date", "item", "amount"])
    return df


def save_data(df):
    df.to_csv("expenses.csv", index=False)


# UI - Calendar and interaction
def calendar_ui(df):
    st.title("📅 가계부 달력")
    today = datetime.date.today()
    year = st.sidebar.selectbox(
        "연도",
        list(range(2020, today.year + 1)),
        index=len(range(2020, today.year + 1)) - 1,
    )
    month = st.sidebar.selectbox("월", list(range(1, 13)), index=today.month - 1)

    st.markdown("### ")
    st.markdown("#### 📆 날짜 선택")
    cal = calendar.monthcalendar(year, month)
    selected_date = st.session_state.get("selected_date", None)

    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            if day == 0:
                cols[i].markdown(" ")
            else:
                if cols[i].button(str(day)):
                    st.session_state["selected_date"] = datetime.date(year, month, day)
                    selected_date = st.session_state["selected_date"]

    if selected_date:
        st.subheader(f"📌 {selected_date.strftime('%Y-%m-%d')} 지출 내역")
        daily_df = df[df["date"] == pd.to_datetime(selected_date)]
        st.table(daily_df)

        uploaded_image = st.file_uploader(
            "영수증 이미지 업로드", type=["jpg", "jpeg", "png"]
        )
        extracted_text = ""

        if uploaded_image:
            image = Image.open(uploaded_image)
            st.image(image, caption="업로드한 영수증", use_container_width=True)
            if st.button("영수증 텍스트 추출"):
                with st.spinner("텍스트 인식 중..."):
                    extracted_text = extract_text_from_image(image)
                    st.session_state["ocr_text"] = extracted_text
                    st.session_state["parsed_items"] = parse_items(extracted_text)
                    st.session_state["total_amount"] = extract_total_amount(
                        extracted_text
                    )

        if "ocr_text" in st.session_state:
            st.text_area("인식된 텍스트", st.session_state["ocr_text"], height=150)

        if "parsed_items" in st.session_state and st.session_state["parsed_items"]:
            st.markdown("**추출된 품목 및 가격**")
            for item, amount in st.session_state["parsed_items"]:
                st.write(f"- {item}: {amount}원")
        elif "total_amount" in st.session_state and st.session_state["total_amount"]:
            st.markdown(f"**총액 추출됨: {st.session_state['total_amount']}원**")
            if st.button("💾 총액만 저장"):
                new_row = pd.DataFrame(
                    [[selected_date, "합계", st.session_state["total_amount"]]],
                    columns=["date", "item", "amount"],
                )
                df = pd.concat([df, new_row], ignore_index=True)
                save_data(df)
                st.success("총액 저장 완료!")
                st.session_state.pop("total_amount", None)
                st.session_state.pop("ocr_text", None)
                st.experimental_rerun()

        item = st.text_input("직접 입력 - 품목")
        price = st.number_input("직접 입력 - 금액", step=100, min_value=0)
        if st.button("직접 추가 저장"):
            if item and price > 0:
                new_row = pd.DataFrame(
                    [[selected_date, item, price]], columns=["date", "item", "amount"]
                )
                df = pd.concat([df, new_row], ignore_index=True)
                save_data(df)
                st.success("직접 입력 저장 완료!")
                st.experimental_rerun()

        if "parsed_items" in st.session_state and st.session_state["parsed_items"]:
            if st.button("💾 저장"):
                for item, amount in st.session_state["parsed_items"]:
                    new_row = pd.DataFrame(
                        [[selected_date, item, amount]],
                        columns=["date", "item", "amount"],
                    )
                    df = pd.concat([df, new_row], ignore_index=True)
                save_data(df)
                st.success("저장 완료!")
                st.session_state.pop("parsed_items", None)
                st.session_state.pop("ocr_text", None)
                st.experimental_rerun()

        if st.button("🗑️ 삭제 (이 날짜 전체)"):
            df = df[df["date"] != pd.to_datetime(selected_date)]
            save_data(df)
            st.success("삭제 완료")
            st.experimental_rerun()

    return df, year, month


# Main
df = load_data()
df, year, month = calendar_ui(df)

# Optional: Summary plot
if st.checkbox("월별 지출 요약 보기"):
    if pd.api.types.is_datetime64_any_dtype(df["date"]):
        monthly_df = df[df["date"].dt.year == year]
        monthly_df = monthly_df[monthly_df["date"].dt.month == month]
        total = monthly_df.groupby("item")["amount"].sum()
        st.bar_chart(total)
    else:
        st.error("'date' 컬럼이 날짜 형식이 아닙니다. CSV 파일을 확인하세요.")
