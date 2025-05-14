import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

st.set_page_config(page_title="와인 알코올 예측기", layout="wide")
st.title("🍷 와인 알코올 도수 예측기 (회귀 분석)")
st.markdown("와인의 다양한 성분을 기반으로 알코올 도수를 예측합니다.")


# 데이터 로딩
@st.cache_data
def load_data():
    data = load_wine(as_frame=True)
    df = data.frame
    df.columns = df.columns.str.replace(" ", "_")
    return df


df = load_data()

# 타겟은 'alcohol'로 설정, 나머지를 입력 변수로
y = df["alcohol"]
X = df.drop(columns=["alcohol"])

# 학습/테스트 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# 모델 선택
st.sidebar.header("🔧 모델 설정")
model_name = st.sidebar.selectbox("회귀 모델 선택", ["Linear", "Ridge", "Lasso"])
alpha = (
    st.sidebar.slider("정규화 강도 (alpha)", 0.01, 10.0, 1.0)
    if model_name != "Linear"
    else None
)

if model_name == "Linear":
    model = LinearRegression()
elif model_name == "Ridge":
    model = Ridge(alpha=alpha)
else:
    model = Lasso(alpha=alpha)

model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# 성능 지표
st.subheader("📊 모델 성능")
col1, col2 = st.columns(2)
col1.metric("R² Score", f"{r2_score(y_test, y_pred):.3f}")
col2.metric("RMSE", f"{mean_squared_error(y_test, y_pred) ** 0.5:.3f}")

# 시각화
st.subheader("🔍 예측 vs 실제")
fig, ax = plt.subplots()
ax.scatter(y_test, y_pred, alpha=0.5)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--")
ax.set_xlabel("실제 알코올 도수")
ax.set_ylabel("예측 도수")
ax.set_title("실제 vs 예측")
st.pyplot(fig)

# 변수 중요도
st.subheader("📌 변수 중요도")
coef = model.coef_
features = X.columns
fig2, ax2 = plt.subplots()
ax2.barh(features, coef)
ax2.set_title("회귀 계수 (Feature Importance)")
st.pyplot(fig2)

# 사용자 입력 예측
st.subheader("🧮 사용자 입력 기반 알코올 예측")
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
    st.success(f"🍷 예측된 알코올 도수: **{prediction:.2f}** %")
