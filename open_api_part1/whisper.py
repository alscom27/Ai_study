import sounddevice as sd
from scipy.io.wavfile import write
from openai import OpenAI
from pathlib import Path
import time

# OpenAI API 클라이언트
client = OpenAI()

# 기본 설정
fs = 16000  # 샘플레이트 (16kHz)
seconds = 5  # 녹음 시간 (초)
filename = "live_input.wav"

# 1. 녹음 시작
print(" 지금부터 5초간 녹음합니다...")
recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype="int16")
sd.wait()
write(filename, fs, recording)
print(" 녹음 완료!")

# 2. Whisper로 한국어 텍스트 변환
with open(filename, "rb") as audio_file:
    transcript = client.audio.transcriptions.create(
        file=audio_file, model="whisper-1", response_format="text", language="ko"
    )
print("인식된 텍스트:", transcript)


print("\n [인식된 자막 - 한국어]")
print(transcript)
# 3. GPT로 영어 번역
messages = [
    {
        "role": "system",
        "content": "Translate the following Korean sentence into natural English.",
    },
    {"role": "user", "content": transcript},
]
translation_response = client.chat.completions.create(
    model="gpt-4o", messages=messages, temperature=0.3  # 또는 "gpt-3.5-turbo"
)
english_translation = translation_response.choices[0].message.content
print("\n [자동 번역 - 영어]")
print(english_translation)
