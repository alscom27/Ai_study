import streamlit as st
import sounddevice as sd
from scipy.io.wavfile import write, read
from openai import OpenAI
from pathlib import Path
import tempfile
import os
import time
import datetime
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# OpenAI API 클라이언트 초기화
client = OpenAI(api_key=api_key)

# 페이지 설정
st.set_page_config(page_title="음성 번역 앱", page_icon="🎙️", layout="wide")

# Streamlit 앱 제목
st.title("음성 녹음 및 번역 앱")
st.write("음성을 녹음하고 텍스트로 변환한 후 영어로 번역합니다.")

# 처리 단계 상태창 설정
status_container = st.container()
with status_container:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        record_status = st.empty()
        record_status.info("📝 녹음 대기 중")
    with col2:
        save_status = st.empty()
        save_status.info("💾 저장 대기 중")
    with col3:
        transcribe_status = st.empty()
        transcribe_status.info("🔊 변환 대기 중")
    with col4:
        translate_status = st.empty()
        translate_status.info("🌐 번역 대기 중")

# API 키 확인
if not api_key:
    st.error(
        "OPENAI_API_KEY가 환경 변수에 설정되지 않았습니다. .env 파일을 확인해주세요."
    )
    st.stop()

# 기본 설정
fs = 16000  # 샘플레이트 (16kHz)
seconds = st.sidebar.slider("녹음 시간 (초)", min_value=1, max_value=30, value=5)

# 파일 저장 위치 설정 (사용자가 선택할 수 있는 옵션 제공)
save_option = st.sidebar.radio(
    "녹음 파일 저장 위치", ["임시 디렉토리", "현재 작업 디렉토리"]
)

if save_option == "임시 디렉토리":
    # 임시 디렉토리 생성
    temp_dir = tempfile.mkdtemp()
    save_dir = temp_dir
elif save_option == "현재 작업 디렉토리":
    save_dir = os.getcwd()

# 타임스탬프를 이용한 고유한 파일 이름 생성
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"recording_{timestamp}.wav"
file_path = os.path.join(save_dir, filename)

# 상태 정보 표시 섹션
file_info_container = st.container()
with file_info_container:
    file_location = st.empty()
    file_playback = st.empty()

# 다국어 선택 기능
nations = {
    "영어": "English",
    "중국어": "Chinese",
    "일본어": "Japanese",
    "프랑스어": "French",
}

with col1:
    seleted_lang = st.selectbox("번역 국가 설정", list(nations.keys()))
    selected_nation = nations[seleted_lang]

# 녹음 기능
with col2:
    if st.button("🎙️ 녹음 시작"):
        # 녹음 상태 업데이트
        record_status.warning("🎙️ 녹음 중...")
        save_status.info("💾 저장 대기 중")
        transcribe_status.info("🔊 변환 대기 중")
        translate_status.info("🌐 번역 대기 중")

        with st.spinner(f"🎙️ {seconds}초 동안 녹음 중..."):
            # 진행 상태 표시
            progress_bar = st.progress(0)
            for i in range(seconds):
                # 1초마다 프로그레스 바 업데이트
                progress_bar.progress((i + 1) / seconds)
                if i == 0:  # 첫 번째 반복에서만 녹음 시작
                    recording = sd.rec(
                        int(seconds * fs), samplerate=fs, channels=1, dtype="int16"
                    )
                time.sleep(1)

            # 녹음 완료 대기
            sd.wait()

            # 녹음 상태 업데이트
            record_status.success("✅ 녹음 완료!")
            save_status.warning("💾 저장 중...")

            # 녹음된 오디오 저장
            write(file_path, fs, recording)

            # 저장 상태 업데이트
            save_status.success("✅ 저장 완료!")

            # 파일 정보 표시
            file_location.success(f"📂 파일 저장 위치: {file_path}")

            # 세션 상태에 녹음 완료 플래그 저장
            st.session_state.recording_done = True
            st.session_state.file_path = file_path

            # 재생 컨트롤 추가
            with file_playback.container():
                st.subheader("🔊 녹음된 파일 재생")
                audio_file = open(file_path, "rb")
                st.audio(audio_file.read(), format="audio/wav")

                # 오디오 파일 길이 확인
                sample_rate, data = read(file_path)
                duration = len(data) / sample_rate
                st.info(f"파일 길이: {duration:.2f}초 / 샘플레이트: {sample_rate}Hz")

                # 수동 재생 버튼 추가
                if st.button("🔊 재생하기"):
                    try:
                        # 오디오 데이터 불러와서 재생
                        sample_rate, data = read(file_path)
                        sd.play(data, sample_rate)
                        st.success("재생 중...")
                        # 재생이 끝날 때까지 대기
                        sd.wait()
                        st.success("재생 완료!")
                    except Exception as e:
                        st.error(f"재생 중 오류 발생: {e}")

        # 자동으로 처리 진행
        st.rerun()

# 텍스트 변환 및 번역 처리
if "recording_done" in st.session_state and st.session_state.recording_done:
    # Whisper로 한국어 텍스트 변환
    transcribe_status.warning("🔊 텍스트 변환 중...")

    with st.spinner("📝 음성을 텍스트로 변환 중..."):
        with open(st.session_state.file_path, "rb") as audio_file:
            try:
                transcript = client.audio.transcriptions.create(
                    file=audio_file,
                    model="whisper-1",
                    response_format="text",
                    language="ko",
                )

                # 변환 상태 업데이트
                transcribe_status.success("✅ 텍스트 변환 완료!")

                # 결과 표시
                st.subheader("📝 인식된 텍스트:")
                st.write(transcript)

                # 세션 상태에 저장
                st.session_state.transcript = transcript
                st.session_state.transcription_done = True
            except Exception as e:
                transcribe_status.error("❌ 텍스트 변환 실패!")
                st.error(f"텍스트 변환 중 오류가 발생했습니다: {e}")
                st.session_state.transcription_done = False

    # GPT로 영어 번역
    if "transcription_done" in st.session_state and st.session_state.transcription_done:
        translate_status.warning(f"🌐 {seleted_lang}로 번역 중...")

        with st.spinner("🌐 텍스트를 영어로 번역 중..."):
            try:
                messages = [
                    {
                        "role": "system",
                        "content": f"Translate the following Korean sentence into natural {selected_nation}.",
                    },
                    {"role": "user", "content": st.session_state.transcript},
                ]

                translation_response = client.chat.completions.create(
                    model="gpt-4o",  # 또는 "gpt-3.5-turbo"
                    messages=messages,
                    temperature=0.3,
                )

                english_translation = translation_response.choices[0].message.content

                # 번역 상태 업데이트
                translate_status.success("✅ 번역 완료!")

                # 결과 표시
                st.subheader(f"🌐 {seleted_lang} 번역:")
                st.write(english_translation)

                # OpenAI TTS 적용
                speech_response = client.audio.speech.create(
                    model="tts-1",
                    voice="shimmer",
                    input=english_translation,  # 다른 목소리로 바꿔도 됨
                )

                tts_path = os.path.join(save_dir, f"tts_{timestamp}.mp3")
                with open(tts_path, "wb") as f:
                    f.write(speech_response.content)

                st.subheader("🔈 번역 결과 음성 재생")
                with open(tts_path, "rb") as audio_file:
                    st.audio(audio_file.read(), format="audio/mp3")

                # 처리 완료 후 상태 유지 (초기화하지 않음)
                # 이전 코드: st.session_state.recording_done = False
                # 이전 코드: st.session_state.transcription_done = False
            except Exception as e:
                translate_status.error("❌ 번역 실패!")
                st.error(f"번역 중 오류가 발생했습니다: {e}")


# 새 녹음 시작 버튼
if "recording_done" in st.session_state and st.session_state.recording_done:
    if st.button("🔄 새 녹음 시작"):
        # 상태 초기화
        st.session_state.recording_done = False
        st.session_state.transcription_done = False
        if "transcript" in st.session_state:
            del st.session_state.transcript

        # 상태창 초기화
        record_status.info("📝 녹음 대기 중")
        save_status.info("💾 저장 대기 중")
        transcribe_status.info("🔊 변환 대기 중")
        translate_status.info("🌐 번역 대기 중")

        # 페이지 새로고침
        st.rerun()

# 사이드바에 추가 정보
with st.sidebar:
    st.subheader("앱 정보")
    st.write("이 앱은 다음 단계로 작동합니다:")
    st.write("1. 음성 녹음")
    st.write("2. 파일 저장 및 재생")
    st.write("3. Whisper AI로 한국어 텍스트 변환")
    st.write("4. GPT로 다국어 번역")
    st.write("5. TTS 음성 재생")

    # 최근 녹음 파일 정보
    if "file_path" in st.session_state:
        st.subheader("현재 녹음 파일 정보")
        st.info(f"파일 이름: {os.path.basename(st.session_state.file_path)}")
        st.info(f"파일 경로: {os.path.dirname(st.session_state.file_path)}")

        # 파일 크기 확인
        if os.path.exists(st.session_state.file_path):
            file_size = os.path.getsize(st.session_state.file_path) / 1024  # KB 단위
            st.info(f"파일 크기: {file_size:.2f} KB")
