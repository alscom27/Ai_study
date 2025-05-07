import cv2
from huggingface_hub import InferenceClient
import streamlit as st
from PIL import Image
import numpy as np
import tempfile

# --- Streamlit 페이지 설정 ---
st.set_page_config(page_title="사물 인식기", layout="centered")
st.title("Hugging Face + OpenCV 사물 인식기")

# --- Hugging Face API 설정 ---

# hugginface api key 연결하기
client = InferenceClient(token=API_TOKEN)
MODEL_ID = "google/vit-base-patch16-224"  # 공개 이미지 분류 모델

# --- 웹캠 캡처 버튼 ---
if st.button("웹캠으로 사물 캡처하기"):
    cap = cv2.VideoCapture(0)
    st.info("3초 후 캡처합니다. 사물을 준비하세요!")
    cv2.waitKey(3000)  # 3초 대기

    ret, frame = cap.read()
    cap.release()

    if ret:
        # BGR → RGB 변환
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 이미지 보여주기
        st.image(frame_rgb, caption="캡처된 이미지", use_container_width=True)

        # 모델에 분류 요청
        st.info("모델이 이미지를 분석 중입니다...")
        try:
            # PIL 이미지 → Bytes로 변환
            img_pil = Image.fromarray(frame_rgb)
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
                img_pil.save(tmp_file.name)
                with open(tmp_file.name, "rb") as img_file:
                    image_bytes = img_file.read()

            result = client.image_classification(image_bytes, model=MODEL_ID)

            st.success("분류 완료")
            for item in result:
                st.markdown(f"**{item['label']}**: {item['score']:.4f}")
        except Exception as e:
            st.error(f"오류 발생: {e}")
    else:
        st.error("웹캠에서 이미지를 캡처할 수 없습니다.")
else:
    st.info("버튼을 클릭하여 사물 이미지를 캡처하고 인식하세요.")
