import streamlit as st
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt
from matplotlib import rc


# 한글 폰트 설정
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# 데이터셋 로드
housing = fetch_california_housing(as_frame=True)
data = housing.frame
X = data.drop("MedHouseVal", axis=1)
y = data["MedHouseVal"]

# 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# streamlit 앱 설정
st.title("California Housing Price Prediction")
st.write(
    "This app trains regression models on the California Housing dataset and displays R2 score and RMSE."
)

# 모델 선택
model_name = st.selectbox(
    "Select Regression Model",
    ["Lasso", "Ridge", "Elastic Net", "Polynomial Regression"],
)

# Polynomial Features 생성(Polynomail Regression용)
if model_name == "Polynomial Regression":
    degree = st.slider("Select Polynomial Degree", min_value=1, max_value=5, value=2)
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    X_train_poly = poly.fit_transform(X_train)
    X_test_poly = poly.transform(X_test)

else:
    X_train_poly = X_train
    X_test_poly = X_test

# 모델 및 파라미터 설정 UI
if model_name == "Lasso":
    alpha_lasso = st.slider(
        "Select Lasso Alpha", min_value=0.001, max_value=10.0, value=1.0, step=0.001
    )
    model = Lasso(alpha=alpha_lasso)

elif model_name == "Ridge":
    alpha_ridge = st.slider(
        "Select Ridge Alpha", min_value=0.001, max_value=10.0, value=1.0, step=0.001
    )
    model = Ridge(alpha=alpha_ridge)

elif model_name == "Elastic Net":
    alpha_elastic = st.slider(
        "Select Elastic Net Alpha",
        min_value=0.001,
        max_value=10.0,
        value=1.0,
        step=0.001,
    )
    l1_ratio = st.slider(
        "Select Elastic Net L1 Ratio", min_value=0.1, max_value=0.9, value=0.5, step=0.1
    )
    model = ElasticNet(alpha=alpha_elastic, l1_ratio=l1_ratio)

elif model_name == "Polynomial Regression":
    model = LinearRegression()

# 모델 학습
try:
    model.fit(X_train, y_train)

    # 예측
    y_pred = model.predict(X_test_poly)

    # 성능 평가
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    # 결과 출력
    st.write(f"###{model_name} Results")
    if model_name == "Lasso":
        st.write(f"Alpha : {alpha_lasso}")
    elif model_name == "Ridge":
        st.write(f"Alpha : {alpha_ridge}")
    elif model_name == "Elastic Net":
        st.write(f"Alpha : {alpha_elastic}, L1 Ratio : {l1_ratio}")
    elif model_name == "Polynomial Regression":
        st.write(f"Degree : {degree}")
    st.write(f"R2 Score : {r2:.4f}")
    st.write(f"RMSE : {rmse:.4f}")

    # 실제 값 vs 예측 값 시각화
    st.write("###Actual vs Predicted Values")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(y_test, y_pred, color="blue", alpha=0.5)
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--", lw=2)
    ax.set_xlabel("실제 값")
    ax.set_ylabel("예측 값")
    ax.set_title(f"{model_name} - 실제 값 vs 예측 값")
    st.pyplot(fig)

except Exception as e:
    st.error(f"An error occurred : {str(e)}")

# 데이터셋 정보
st.write("###Dataset Info")
st.write(f"Features : {X.columns.tolist()}")
st.write(f"Number of Samples : {len(data)}")
st.write(f"Target : Median House Value (in $100,000s)")

# 학습 버튼 (새로고침 역할)
if st.button("Retrain Model"):
    st.rerun()
