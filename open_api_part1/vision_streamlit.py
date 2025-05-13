import streamlit as st
import base64
import sounddevice as sd
from scipy.io.wavfile import write
import openai
import tempfile
import os
import time
from io import BytesIO
import numpy as np
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=api_key)

# 페이지 설정
st.set_page_config(page_title="멀티모달 어시스턴트", page_icon="🤖", layout="wide")

# 타이틀 및 소개
st.title("🤖 멀티모달 어시스턴트")
st.write("이미지에 대해 질문하고 음성으로 답변을 들어보세요!")

# 세션 상태 초기화
if "conversations" not in st.session_state:
    st.session_state.conversations = []
if "current_image" not in st.session_state:
    st.session_state.current_image = None
if "chat_active" not in st.session_state:
    st.session_state.chat_active = False

# 사이드바: OpenAI API 키 입력
with st.sidebar:
    st.header("설정")

    # 녹음 설정
    st.subheader("녹음 설정")
    seconds = st.slider("녹음 시간 (초)", min_value=1, max_value=10, value=5)
    fs = st.selectbox("샘플링 레이트", [16000, 22050, 44100], index=0)

# 메인 화면 분할
col1, col2 = st.columns([1, 1])

# 이미지 업로드 섹션
with col1:
    st.header("이미지 업로드")
    uploaded_file = st.file_uploader(
        "이미지를 업로드하세요", type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        st.image(uploaded_file, caption="업로드된 이미지", use_container_width=True)
        st.session_state.current_image = uploaded_file.getvalue()
        st.session_state.chat_active = True

        if st.button("새 대화 시작"):
            st.session_state.conversations = []
            st.rerun()

# 실시간 녹음 섹션
with col2:
    st.header("질문하기")
    text_question = st.text_input("텍스트로 질문:", key="text_question")
    st.subheader("또는 음성으로 질문:")

    if st.button("🎙️ 녹음 시작"):
        if st.session_state.current_image is None:
            st.error("먼저 이미지를 업로드해주세요!")
        else:
            with st.spinner(f"🎙️ {seconds}초 동안 녹음 중..."):
                temp_audio_file = tempfile.NamedTemporaryFile(
                    delete=False, suffix=".wav"
                )
                temp_audio_filename = temp_audio_file.name
                temp_audio_file.close()

                progress = st.progress(0)
                recording = sd.rec(
                    int(seconds * fs), samplerate=fs, channels=1, dtype="int16"
                )
                for i in range(seconds):
                    progress.progress((i + 1) / seconds)
                    time.sleep(1)
                sd.wait()
                write(temp_audio_filename, fs, recording)
                st.success("✅ 녹음 완료!")

                try:
                    with open(temp_audio_filename, "rb") as audio_file:
                        transcript = client.audio.transcriptions.create(
                            file=audio_file,
                            model="whisper-1",
                            language="ko",
                            response_format="text",
                        )
                    st.session_state.current_question = transcript.strip()
                    st.write(f"🙋 인식된 질문: {st.session_state.current_question}")

                except Exception as e:
                    st.error(f"음성 인식 중 오류가 발생했습니다: {e}")
                finally:
                    os.unlink(temp_audio_filename)

    if st.button("종료", key="quit_button"):
        st.session_state.chat_active = False
        st.write("대화를 종료합니다. 새로운 대화를 시작하려면 페이지를 새로고침하세요.")
        st.stop()


# 질문 처리 함수
def process_question(question):
    if st.session_state.current_image is None:
        st.error("이미지가 없습니다. 먼저 이미지를 업로드해주세요.")
        return

    base64_image = base64.b64encode(st.session_state.current_image).decode("utf-8")

    with st.spinner("🔍 GPT가 이미지를 분석중..."):
        try:
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": question},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                },
                            },
                        ],
                    }
                ],
            )

            english_description = completion.choices[0].message.content

            translation = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "Translate the following English text into natural Korean.",
                    },
                    {"role": "user", "content": english_description},
                ],
            )

            korean_translation = translation.choices[0].message.content.strip()

            response = client.audio.speech.create(
                model="tts-1", voice="nova", input=korean_translation
            )

            st.session_state.conversations.append(
                {
                    "question": question,
                    "answer": korean_translation,
                    "audio": response.content,
                }
            )

            return korean_translation, response.content

        except Exception as e:
            st.error(f"처리 중 오류가 발생했습니다: {e}")
            return None, None


current_question = None
if text_question:
    current_question = text_question
elif "current_question" in st.session_state:
    current_question = st.session_state.current_question
    st.session_state.current_question = None

if current_question and st.session_state.chat_active:
    answer, audio_content = process_question(current_question)
    if answer and audio_content:
        st.session_state.text_question = ""

if st.session_state.conversations:
    st.header("대화 기록")
    for i, conv in enumerate(st.session_state.conversations):
        with st.expander(
            f"질문 {i+1}: {conv['question']}",
            expanded=(i == len(st.session_state.conversations) - 1),
        ):
            st.write(conv["answer"])
            st.audio(conv["audio"], format="audio/mp3")
