import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import time
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2,
    preprocess_input,
    decode_predictions,
)
from tensorflow.keras.preprocessing import image as keras_image

# Matplotlib 한글 폰트 설정
matplotlib.rcParams["font.family"] = "Malgun Gothic"
matplotlib.rcParams["axes.unicode_minus"] = False

# Streamlit 페이지 설정
st.set_page_config(page_title="이미지 분석 대시보드", page_icon="🖼️", layout="wide")


# 모델 로드
@st.cache_resource
def load_model():
    model = MobileNetV2(weights="imagenet")
    return model


model = load_model()

# 제목 표시
st.title("🖼️ 이미지 인식 및 분석 대시보드")

# 파일 업로드
uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="업로드한 이미지", use_container_width=True)

    # 이미지 전처리
    img_resized = img.resize((224, 224))
    img_array = keras_image.img_to_array(img_resized)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # 분석 시뮬레이션
    progress_bar = st.progress(0)
    status_text = st.empty()
    confidences = []

    for percent in range(1, 101):
        if percent % 10 == 0:
            preds = model.predict(img_array)
            confidence = np.max(preds) * 100
            confidences.append(confidence)
        status_text.text(f"분석 진행률: {percent}%")
        progress_bar.progress(percent)
        time.sleep(0.02)

    # 최종 예측 결과
    preds = model.predict(img_array)
    decoded_preds = decode_predictions(preds, top=1)[0][0]
    label = decoded_preds[1]
    confidence = decoded_preds[2] * 100

    st.success(f"✅ 이 이미지는 **{label}** 입니다. (정확도: {confidence:.2f}%)")

    # 정확도 변화 차트
    st.subheader("📈 분석 과정 중 정확도 변화")
    fig, ax = plt.subplots()
    steps = np.arange(10, 101, 10)
    ax.plot(steps, confidences, marker="o")
    ax.set_xlabel("분석 진행률(%)")
    ax.set_ylabel("정확도(%)")
    ax.set_title("분석 중 정확도 변화")
    st.pyplot(fig)
else:
    st.subheader("👋 이미지를 업로드해주세요!")
    st.info("왼쪽 상단 메뉴에서 이미지를 선택하여 업로드하면 분석이 시작됩니다.")

# Footer
st.markdown("---")
st.caption("Made by LJJ")
