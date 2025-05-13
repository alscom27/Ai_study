from openai import OpenAI
from dotenv import load_dotenv
import openai
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=api_key)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What are in these images? Is there any unusual fact?",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://www.domin.co.kr/news/photo/202205/1380435_517885_304.jpg",
                    },
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://cdn.nongupin.co.kr/news/photo/202409/201918_61680_1019.png",
                    },
                },
            ],
        }
    ],
    max_tokens=300,
)
print(response.choices[0].message.content)
