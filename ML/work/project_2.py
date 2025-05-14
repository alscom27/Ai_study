import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# 한글 폰트 설정 (윈도우 기준)
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
st.subheader("📊 선택한 모델 성능")
col1, col2 = st.columns(2)
col1.metric("R² Score", f"{r2_score(y_test, y_pred):.3f}")
rmse = mean_squared_error(y_test, y_pred) ** 0.5
col2.metric("RMSE", f"{rmse:.3f}")

# 모델 성능 비교표
st.subheader("📋 전체 모델 성능 비교")
models = {
    "Linear": LinearRegression(),
    "Ridge": Ridge(alpha=1.0),
    "Lasso": Lasso(alpha=1.0),
}
results = []
for name, m in models.items():
    pipeline = make_pipeline(StandardScaler(), m)
    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)
    results.append(
        {
            "모델": name,
            "R²": r2_score(y_test, preds),
            "RMSE": mean_squared_error(y_test, preds) ** 0.5,
        }
    )
results_df = pd.DataFrame(results)
st.dataframe(results_df.style.format({"R²": "{:.3f}", "RMSE": "{:.3f}"}))

# 시각화: 예측 vs 실제 / 중요도
# col1, col2 = st.columns(2)
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.subheader("🔍 실제값 vs 예측값")
    fig1, ax1 = plt.subplots()
    ax1.scatter(y_test, y_pred, alpha=0.3)
    ax1.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--")
    ax1.set_xlabel("실제값")
    ax1.set_ylabel("예측값")
    ax1.set_title("실제값 vs 예측값")
    st.pyplot(fig1)

with c3:
    # 잔차 분석
    st.subheader("📉 잔차 분석")
    residuals = y_test - y_pred
    fig3, ax3 = plt.subplots()
    ax3.scatter(y_pred, residuals, alpha=0.3)
    ax3.axhline(0, linestyle="--", color="red")
    ax3.set_xlabel("예측값")
    ax3.set_ylabel("잔차")
    ax3.set_title("잔차 분석")
    st.pyplot(fig3)

with c2:
    st.subheader("📌 변수 중요도")
    coef = model.coef_
    features = X.columns
    fig2, ax2 = plt.subplots()
    ax2.barh(features, coef)
    ax2.set_title("회귀 계수 (Feature Importance)")
    st.pyplot(fig2)

with c4:
    # PCA 시각화
    st.subheader("🌀 PCA 특성 분포 (2차원)")
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)
    fig4, ax4 = plt.subplots()
    sc = ax4.scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap="coolwarm", alpha=0.4)
    plt.colorbar(sc, ax=ax4, label="집값 중간값")
    ax4.set_title("PCA로 투영한 특성 시각화")
    st.pyplot(fig4)


# 사용자 입력에 따른 예측
st.subheader("🧮 사용자 입력 기반 예측")
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
    if prediction < 0:
        st.warning("예측된 집값이 0보다 작습니다. 입력값을 다시 확인하세요.")
    else:
        st.success(f"🏠 예측된 집값 (중간값 기준): **${prediction * 100_000:,.0f}**")
