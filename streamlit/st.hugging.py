import streamlit as st
from huggingface_hub import InferenceClient
from PIL import Image
import matplotlib.pyplot as plt
import time


# Matplotlib 한글 폰트 설정
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# --- 페이지설정 ---
st.set_page_config(page_title="이미지 분류 with Hugging Face", layout="centered")
st.title("Hugging Face 이미지 분류기")

# --- Hugging Face API 설정 ---
# hugging face api 키 연결하기
client = InferenceClient(token=API_TOKEN)

# --- 이미지 업로드 ---
uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="업로드된 이미지", use_container_width=True)
    image_bytes = uploaded_file.read()

    with st.spinner("분류 중입니다..."):
        try:
            # --- 이미지 분류 요청 ---
            results = client.image_classification(
                image_bytes, model="google/vit-base-patch16-224"
            )

            st.success("분류 완료!")

            # --- 결과 출력 ---
            for result in results:
                st.markdown(f"**{result['label']}**: {result['score']:.4f}")

            # st.write(results)

            # --- 정확도 시각화 ---
            st.subheader("정확도 시각화")
            if (
                isinstance(results, list)
                and isinstance(results[0], dict)
                and "label" in results[0]
            ):
                labels = [res["label"] for res in results]
                scores = [res["score"] for res in results]

                fig, ax = plt.subplots()
                bars = ax.barh(labels, scores, color="skyblue")
                ax.invert_yaxis()
                ax.set_xlim(0, 1)
                ax.set_xlabel("정확도")
                ax.set_title("Top 분류 결과")

                for bar in bars:
                    ax.text(
                        bar.get_width() + 0.01,
                        bar.get_y() + bar.get_height() / 2,
                        f"{bar.get_width():.2f}",
                        va="center",
                    )

                st.pyplot(fig)
            else:
                st.error("결과 형식이 올바르지 않습니다.")

        except Exception as e:
            st.error(f"오류 발생: {e}")
else:
    st.info("왼쪽에서 이미지를 업로드해 주세요.")
