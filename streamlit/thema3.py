import streamlit as st
import pandas as pd

# 1. 페이지 제목
st.title("데이터프레임 튜토리얼")

# 2. dataframe 생성
df_scores = pd.DataFrame(
    {
        "이름": ["홍길동", "김철수", "이영희", "박민수"],
        "수학": [85, 90, 78, 92],
        "영어": [88, 75, 95, 80],
    }
)

st.subheader("데이터프레임 출력 (인터랙티브)")
st.dataframe(df_scores, use_container_width=True)

# 3. 정적 테이블 출력
st.subheader("테이블 출력 (정적)")
st.table(df_scores)

# 4. 지표 출력
st.subheader("단일 메트릭 예시")
st.metric(label="주간 평균 점수", value="84점", delta="2점 증가")
st.metric(label="수학 최고 점수", value="92점", delta="+4점")

# 5. 컬럼을 이용한 메트릭 정렬
st.subheader("과목별 점수 변화")

# 세 개의 컬럼 생성
c1, c2, c3 = st.columns(3)

c1.metric(label="수학 평균", value="86.3", delta="+2.1")
c2.metric(label="영어 평균", value="84.5", delta="-1.0")
c3.metric(label="전체 평균", value="85.4", delta="+0.6")
