# Streamlit 기반 영수증 자동 입력 가계부
import streamlit as st
import pandas as pd
import cv2
import numpy as np
import openai
import os
from PIL import Image
import matplotlib.pyplot as plt
from datetime import datetime
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# OpenAI API 설정 (client 사용)
client = openai.OpenAI(api_key=api_key)

# 기본 설정
st.set_page_config(page_title="영수증 자동 입력 가계부", layout="wide")

# 데이터 저장 경로
DATA_PATH = "data/receipts.csv"

# 데이터 로드
if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
else:
    df = pd.DataFrame(
        columns=[
            "날짜",
            "품목명",
            "금액",
            "카테고리",
            "언어",
            "전처리 전 정확도",
            "전처리 후 정확도",
        ]
    )


# OpenAI Vision API로 텍스트 추출 함수
def extract_text_from_image(image_file):
    response = client.Image.create(file=image_file, purpose="image-to-text")
    return response["text"]


# OpenAI GPT로 텍스트 분석 함수
def process_receipt_text(receipt_text):
    prompt = f"영수증 텍스트: {receipt_text}\n품목과 금액을 추출해 주세요."
    response = client.Completion.create(
        engine="text-davinci-003", prompt=prompt, max_tokens=100
    )
    return response["choices"][0]["text"].strip()


# 파일 업로드
st.title("📂 영수증 자동 입력 가계부")
uploaded_files = st.file_uploader(
    "영수증 이미지를 업로드하세요",
    type=["jpg", "png", "jpeg"],
    accept_multiple_files=True,
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        st.image(image, caption="업로드한 영수증", use_column_width=True)

        # OpenAI Vision API로 텍스트 추출
        text = extract_text_from_image(uploaded_file)
        result = process_receipt_text(text)
        st.text(f"추출 결과: {result}")

        # 데이터 저장
        df = df.append(
            {
                "날짜": datetime.now().strftime("%Y-%m-%d"),
                "품목명": "추출된 품목",
                "금액": "추출된 금액",
                "카테고리": "기타",
                "언어": "한국어",
                "전처리 전 정확도": 0.0,
                "전처리 후 정확도": 0.0,
            },
            ignore_index=True,
        )
        df.to_csv(DATA_PATH, index=False)
        st.success("영수증 데이터가 성공적으로 저장되었습니다!")

# 데이터 표시
st.header("💾 가계부 데이터")
st.dataframe(df)
