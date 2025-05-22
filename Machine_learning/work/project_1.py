import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# 한글 폰트 설정
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# 페이지 설정
st.set_page_config(page_title="캘리포니아 집값 예측기", layout="wide")
st.title("🏡 캘리포니아 집값 예측기 (회귀 분석)")
st.markdown("선형 회귀 기반으로 캘리포니아의 집값을 예측하는 Streamlit 앱입니다.")


# 데이터 로딩
@st.cache_data
def load_data():
    data = fetch_california_housing(as_frame=True)
    df = data.frame
    df.columns = df.columns.str.replace(" ", "_")
    return df


df = load_data()

# 특성과 타겟
X = df.drop(columns=["MedHouseVal"])
y = df["MedHouseVal"]

# 학습 / 테스트 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# 회귀 모델 선택
st.sidebar.header("🔧 모델 및 설정")
model_name = st.sidebar.selectbox(
    "회귀 모델 선택", ["Linear Regression", "Ridge Regression", "Lasso Regression"]
)

alpha = (
    st.sidebar.slider("정규화 강도 (alpha)", 0.01, 10.0, 1.0)
    if model_name != "Linear Regression"
    else None
)

if model_name == "Linear Regression":
    model = LinearRegression()
elif model_name == "Ridge Regression":
    model = Ridge(alpha=alpha)
else:
    model = Lasso(alpha=alpha)

model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# 성능 출력
st.subheader("📊 모델 성능")
col1, col2 = st.columns(2)
col1.metric("R² Score", f"{r2_score(y_test, y_pred):.3f}")
col2.metric("RMSE", f"{mean_squared_error(y_test, y_pred):.3f}")

col1, col2 = st.columns(2)

with col1:
    # 예측 vs 실제 시각화
    st.subheader("🔍 실제값 vs 예측값")
    fig1, ax1 = plt.subplots()
    ax1.scatter(y_test, y_pred, alpha=0.3)
    ax1.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--")
    ax1.set_xlabel("실제값")
    ax1.set_ylabel("예측값")
    ax1.set_title("실제값 vs 예측값")
    st.pyplot(fig1)

with col2:
    # 변수 중요도 시각화
    st.subheader("📌 변수 중요도")
    coef = model.coef_
    features = X.columns
    fig2, ax2 = plt.subplots()
    ax2.barh(features, coef)
    ax2.set_title("회귀 계수 (Feature Importance)")
    st.pyplot(fig2)

# 사용자 입력에 따른 예측
st.subheader("🧮 사용자 입력을 통한 예측")
user_inputs = {}
with st.form("predict_form"):
    for col in X.columns:
        min_val = float(df[col].min())
        max_val = float(df[col].max())
        mean_val = float(df[col].mean())
        user_inputs[col] = st.slider(col, min_val, max_val, mean_val)
    submitted = st.form_submit_button("예측하기")

if submitted:
    user_df = pd.DataFrame([user_inputs])
    prediction = model.predict(user_df)[0]
    st.success(f"🏠 예측된 집값 (중간값 기준): **${prediction * 100_000:,.0f}**")
