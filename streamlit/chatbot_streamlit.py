# streamlit을 활용한 챗봇
#  pip install streamlit
import streamlit as st

# pip install konlpy
# + Java 기반으로 동작하는 분석기를 사용하기 때문에 JVM필요
# 그래서 자바 설치하고 환경변수 잡음 (JDK 8버전이 제일 안정적)
# konlpy : 한국어 형태소 분석을 파이썬에서 할 수 있게 해주는 오픈소스 NLP(자연어 처리) 라이브러리
# 문장에서 단어 추출, 조사 분리, 품사 태깅, 명사만 추출 등을 함
from konlpy.tag import Okt  # jvm으로 돌아가는거기 때문에 바다야함 1.8대 추천
import time
import requests
import random
import re

# pip install transformers sentencepiece torch
from transformers import pipeline

# 페이지 기본 설정
st.set_page_config(page_title="ChatBot", layout="wide")

# 캐릭터 이미지
characters = {
    "3스타 쉐프": [
        "안성재",
        "https://img.khan.co.kr/news/2024/10/23/l_2024102301000679900063701.jpg",
    ],
    "불안핑": [
        "윤남노",
        "https://i.namu.wiki/i/YEr_K9uN-yXUwvjjTwPKZRnJeSQAcJ01il5Byjt0nbLF49EoYFTpWlZMOBdNmD6ucIp0wyvoLVLe5bt5eFwjwg.webp",
    ],
    "논란의 중심": [
        "백모씨",
        "https://dimg.donga.com/wps/NEWS/IMAGE/2024/10/17/130239330.2.png",
    ],
}

user_avatar_url = "https://png.pngtree.com/png-vector/20191009/ourmid/pngtree-user-icon-png-image_1796659.jpg"
assistant_avatar_url = (
    "https://img.freepik.com/free-vector/chatbot-chat-message-vectorart_78370-4104.jpg"
)

# HTML 스타일
st.markdown(
    """<style>
    .chat-bubble{
        padding:10px;
        margin:5px;
        border-radius:10px;
        max-width:70%;
        word-wrap:break-word;
        display:flex;
        align-items:flex-start;
        overflow-wrap:break-word;
        }
    .chat-avatar{
        width:50px;
        height:50px;
        border-radius:50%;
        margin-right:10px;
        object-fit:cover;
        }
    .user-bubble{
        background-color:gray;
        color:black;
        border-top-right-radius:0;
        margin-left:auto;
        flex-direction:row-reverse;
        gap:10px;
        }
    .assistant-bubble{
        background-color:gray;
        color:black;
        border-top-left-radius:0;
        margin-right:auto;
        gap:10px;
        }
    .user-message{
            align-self:flex-end;
            }
    .assistant-message{
        align-self:flex-start;
        }
</style>""",
    unsafe_allow_html=True,
)


# 요약기 불러오기
def load_summarizer():
    return pipeline("summarization", model="digit82/kobart-summarization")


# 대화내용 요약
def summarize_conversation(messages):
    summarizer = load_summarizer()
    full_text = "\n".join([f"{m['role']}: {m['content']}" for m in messages])[:500]
    prompt = f"다음 대화 내용을 보고, 한 문장짜리 매우 짧은 한국어 제목을 만들어주세요.\n\n{full_text}"
    summary = summarizer(prompt, max_length=15, min_length=10, do_sample=False)
    return summary[0]["summary_text"]


# 요리명으로 대화제목 만들기.. 위에 summarizer가 너무 멍청함...
def generate_title_from_recipes(response_text):
    matches = re.findall(r"📋 요리명 : (.+?)\n", response_text)
    if matches:
        return matches[0]  # 가장 먼저 등장한 요리명
    return "사용자와 대화"


# 말풍선 스타일 메세지 표시 함수
def display_chat_message(role, content, avatar_url):
    bubble_class = "user-bubble" if role == "user" else "assistant-bubble"
    message_class = "user-message" if role == "user" else "assistant-message"
    st.markdown(
        f"""<div class="chat-bubble {bubble_class} {message_class}"><img src="{avatar_url}" class="chat-avatar"><div>{content}</div></div>""",
        unsafe_allow_html=True,
    )


# json 파싱 함수
def json_parsing():
    # 인증키
    service_key = "71efe28b43424ed79f88"
    # api 요청 주소
    url = f"http://openapi.foodsafetykorea.go.kr/api/{service_key}/COOKRCP01/json/1/100"
    # 요청 보내기
    response = requests.get(url)

    # 응답 확인
    if response.status_code == 200:
        data = response.json()

        items = data["COOKRCP01"]["row"]
    else:
        print("API 요청 실패 :", response.status_code)

    return items if response.status_code == 200 else response.status_code


# 단어가 한글자만 포함되도 매치 점수가 올라서 정확히 일차하면 카운트되게 수정
def word_in_text(word, text):
    return re.search(rf"\b{re.escape(word)}\b", text) is not None


# 대화 생성 함수
def generate_conversation(user_input):
    assistant_content = ""
    # 심심하니까 랜덤 문구들
    random_content = [
        "몇 가지 추천 레시피를 알려드릴게요. 😄\n",
        "추천 레시피를 알려드리겠습니다! 😎\n",
        "음...몇 가지 추천 요리들을 알려드릴게요. 🤔\n",
    ]
    # 매치 점수 저장 리스트
    scored_items = []

    # 사용자 대화내용 분석
    okt = Okt()
    tokens = okt.pos(user_input, stem=True)

    # 사용자 대화내용 키워드 분류
    nouns = [word for word, tag in tokens if tag == "Noun"]
    verbs = [word for word, tag in tokens if tag == "Verb"]

    # 형태소 분석기가 분석한 굽다와 json데이터의 굽기 가 매치 되지않아서 기를 다로 수정
    verb_methods = [verb[:1] + "기" for verb in verbs if verb.endswith("다")]

    # 데이터 가져오기
    items = json_parsing()
    # 데이터 돌면서 매치 점수 계산
    for item in items:
        score = 0
        name = item["RCP_NM"]
        ingredient = item["RCP_PARTS_DTLS"]
        method = item["RCP_WAY2"]

        # 음식명과 명사 키워드 일치시 매치점수 +1
        if any(word_in_text(noun, name) for noun in nouns):
            score += 1
        # 재료와 명사 일치시
        if any(word_in_text(noun, ingredient) for noun in nouns):
            score += 1
        # 조리방법과 동사 키워드 일치시
        if any(verb_method in method for verb_method in verb_methods):
            score += 1

        # 매치점수가 0보다 큰 것(언급된건) 전부 리스트로 등록
        if score > 0:
            scored_items.append((score, item))
    # 매치점수 높은 순으로 정렬
    # 키를 기준으로 내림차순
    scored_items.sort(key=lambda x: x[0], reverse=True)

    # 매치 점수 높은 5개 출력
    top_items = scored_items[:5]

    # 추천 레시피가 없으면
    if bool(top_items) == False:
        assistant_content = "추천드릴 레시피가 없습니다. 😢\n"
    # 추천 레시피가 있으면
    else:
        # randomint(x,y) x부터 y이하...
        assistant_content += (
            f"{random_content[random.randint(0,len(random_content)-1)]}"
        )
        for score, item in top_items:
            # 매치점수 : {score}\n
            assistant_content += f"""
✅ 매치 점수 : {score}\n
📋 요리명 : {item['RCP_NM']}\n
재료 : {item['RCP_PARTS_DTLS']}\n
조리법 : {item['RCP_WAY2']}\n
{'-'*20}\n

"""

    assistant_content += "\n💡 더 궁금하신게 있으면 물어봐주세요!"
    return assistant_content


st.title("🧠 챗봇")
# 개체 설정 세션 상태 초기화
if "chat_storage" not in st.session_state:
    st.session_state.chat_storage = []
if "messages" not in st.session_state:
    st.session_state.messages = []
if "stage" not in st.session_state:
    st.session_state.stage = 1
if "character" not in st.session_state:
    st.session_state.character = None
if "character_avatar_url" not in st.session_state:
    st.session_state.character_avatar_url = assistant_avatar_url

if "saveed" not in st.session_state:
    st.session_state.saved = False

# 사이드바 (대화목록(대화제목), 새대화버튼, 대화목록 삭제 버튼)
with st.sidebar:
    st.write("#### 💬 대화 목록")
    if st.button("➕ 새 대화"):
        st.session_state.messages = []
        st.session_state.stage = 1
        st.session_state.saved = False
        st.rerun()
    for i, chat in enumerate(st.session_state.chat_storage):
        col1, col2 = st.columns([4, 1])
        with col1:
            if st.button(chat["title"], key=f"load_chat_{i}"):
                st.session_state.messages = chat["messages"].copy()
                st.session_state.character_avatar_url = chat.get("avatar")
                st.session_state.stage = 2
                st.session_state.saved = True
                st.rerun()
        with col2:
            if st.button("🗑", key=f"delete_chat_{i}"):
                del st.session_state.chat_storage[i]
                st.session_state.stage = 1
                st.rerun()

# 메인화면 캐릭터 선택 후 assistant 기본 문구 출력
if st.session_state.stage == 1:
    st.markdown("<h3>캐릭터를 선택하세요:</h3>", unsafe_allow_html=True)
    for character, info in characters.items():
        if st.button(f"{character} 선택"):
            st.session_state.character = character
            st.session_state.character_avatar_url = info[1]
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": f"안녕하세요! {character}입니다. 무엇을 도와드릴까요?",
                }
            )
            st.session_state.stage = 2
            st.rerun()

# 대화 입출력
elif st.session_state.stage == 2:
    for msg in st.session_state.messages:
        display_chat_message(
            msg["role"],
            msg["content"],
            (
                st.session_state.character_avatar_url
                if msg["role"] == "assistant"
                else user_avatar_url
            ),
        )
    user_input = st.chat_input("대화를 입력하세요:")
    if user_input:
        st.session_state.messages.append(
            {"role": "user", "content": user_input, "avatar": user_avatar_url}
        )
        with st.spinner("답변 생성 중..."):
            time.sleep(2)
            response = generate_conversation(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})
        if st.session_state.saved == False:
            # title = summarize_conversation(st.session_state.messages)
            title = generate_title_from_recipes(response)
            st.session_state.chat_storage.append(
                {
                    "title": title,
                    "messages": st.session_state.messages.copy(),
                    "avatar": st.session_state.character_avatar_url,
                }
            )
            st.session_state.saved = True
        st.rerun()


# # ############# 개선 사항
# 1. 매 채팅마다 제목이 붙는 현상
# 2. 파싱해오는 json은 형태소 분석기를 거치지 않아서 불일치 하지 않아야하는 정보가 불일치되는 현상
