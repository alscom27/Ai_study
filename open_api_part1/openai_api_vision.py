import base64
from openai import OpenAI
from dotenv import load_dotenv
import openai
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=api_key)


# 이미지 인코딩 함수
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# 이미지 경로
image_path = "images/person1.jpg"
# 이미지 Base64 인코딩
base64_image = encode_image(image_path)
# 1단계: GPT로 이미지 내용 분석 (영어)
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
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
# 영어 결과 추출
english_description = completion.choices[0].message.content
print(" 분석 결과 (영어):\n", english_description)
# 2단계: 한국어로 번역
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
korean_translation = translation.choices[0].message.content
print("\n 번역 결과 (한국어):\n", korean_translation)
