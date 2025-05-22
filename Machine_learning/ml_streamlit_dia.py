# -------------------------- 기존 코드 상단 + 수정 -------------------------------
import streamlit as st
import numpy as np
import pandas as pd
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt
import seaborn as sns

# matplotlib 한글 깨짐 방지
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

st.set_page_config(layout="wide")

# -------------------------- 데이터 로드 및 분할 -------------------------------
data = load_diabetes(as_frame=True)
df = data.frame
X = df.drop("target", axis=1)
y = df["target"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

st.title("🧪 당뇨병 진행 예측 - 회귀 모델 학습 앱")
st.markdown(
    """
이 앱은 **선형 회귀 모델**을 학습하고 결과를 시각화하여 **모델을 해석하고 이해하는 학습용 도구**입니다.
- 다양한 회귀 모델을 선택하고,  
- 데이터를 학습한 후,  
- 예측 성능과 변수 중요도를 분석할 수 있습니다.
"""
)

# -------------------------- 모델 선택 -------------------------------
model_name = st.selectbox(
    "🔍 회귀 모델 선택", ["Lasso", "Ridge", "Elastic Net", "Polynomial Regression"]
)


# -------------------------- 모델 설명 -------------------------------
def show_model_description(name):
    with st.expander("📘 선택한 모델 설명"):
        if name == "Lasso":
            st.markdown(
                "**Lasso 회귀**는 L1 정규화를 사용해 일부 계수를 0으로 만들어 변수 선택 효과를 가집니다."
            )
            st.latex(r"J(\theta) = \sum(y_i - \hat{y}_i)^2 + \lambda \sum|\theta_j|")
        elif name == "Ridge":
            st.markdown(
                "**Ridge 회귀**는 L2 정규화를 사용해 모든 계수를 작게 유지시킵니다."
            )
            st.latex(r"J(\theta) = \sum(y_i - \hat{y}_i)^2 + \lambda \sum\theta_j^2")
        elif name == "Elastic Net":
            st.markdown(
                "**Elastic Net**은 L1 + L2를 결합해 변수 선택과 정규화를 동시에 수행합니다."
            )
            st.latex(
                r"J(\theta) = \sum(y_i - \hat{y}_i)^2 + \alpha(\lambda_1 \sum|\theta_j| + \lambda_2 \sum\theta_j^2)"
            )
        elif name == "Polynomial Regression":
            st.markdown(
                "**다항 회귀**는 입력 변수를 거듭제곱하여 비선형 관계를 선형 회귀로 학습합니다."
            )
            st.latex(
                r"\hat{y} = \theta_0 + \theta_1x + \theta_2x^2 + ... + \theta_nx^n"
            )


show_model_description(model_name)

# -------------------------- 하이퍼파라미터 설정 -------------------------------
if model_name == "Polynomial Regression":
    degree = st.slider("다항식 차수 선택", 1, 5, 2)
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    X_train_poly = poly.fit_transform(X_train)
    X_test_poly = poly.transform(X_test)
    model = LinearRegression()
else:
    X_train_poly = X_train
    X_test_poly = X_test
    alpha = st.slider("정규화 강도 (알파 값)", 0.001, 10.0, 1.0, 0.001)
    if model_name == "Lasso":
        model = Lasso(alpha=alpha)
    elif model_name == "Ridge":
        model = Ridge(alpha=alpha)
    elif model_name == "Elastic Net":
        l1_ratio = st.slider("L1 비율", 0.1, 0.9, 0.5, 0.1)
        model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio)

# -------------------------- 모델 학습 및 예측 -------------------------------
model.fit(X_train_poly, y_train)
y_pred = model.predict(X_test_poly)

# -------------------------- 성능 평가 -------------------------------
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)

st.markdown("### 📊 모델 성능 지표")
st.markdown(
    f"""
- **R² (설명력)**: {r2:.4f} → 1에 가까울수록 좋음  
- **RMSE (평균 제곱근 오차)**: {rmse:.4f} → 예측값과 실제값 차이의 표준편차  
- **MAE (평균 절대 오차)**: {mae:.4f} → 직관적으로 해석 가능한 평균 예측 오차
"""
)

# -------------------------- 예측 vs 실제 시각화 -------------------------------
col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.scatterplot(x=y_test, y=y_pred, ax=ax, color="blue", alpha=0.6)
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--")
    ax.set_title("실제 값 vs 예측 값")
    ax.set_xlabel("실제 값")
    ax.set_ylabel("예측 값")
    st.pyplot(fig)

with col2:
    residuals = y_test - y_pred
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.histplot(residuals, bins=20, kde=True, ax=ax, color="purple")
    ax.set_title("잔차 분포 (오차)")
    st.pyplot(fig)

# -------------------------- 회귀 계수 시각화 -------------------------------
if model_name != "Polynomial Regression" or degree <= 2:
    try:
        st.markdown("### 🔍 특성 중요도 (회귀 계수)")
        coef = model.coef_
        feature_names = (
            poly.get_feature_names_out(X.columns)
            if model_name == "Polynomial Regression"
            else X.columns
        )
        coef_df = pd.Series(coef, index=feature_names).sort_values()
        fig, ax = plt.subplots(figsize=(8, 5))
        coef_df.plot(kind="barh", ax=ax, color="teal")
        ax.set_title("회귀 계수 크기 (클수록 영향력 ↑)")
        st.pyplot(fig)
    except Exception as e:
        st.warning("회귀 계수를 시각화할 수 없습니다.")

# -------------------------- 모델 비교 기능 -------------------------------
st.markdown("## 🔬 모델 성능 비교 실험")

if st.checkbox("📊 모든 모델 학습 & 비교하기"):
    compare_models = {
        "Lasso": Lasso(alpha=1.0),
        "Ridge": Ridge(alpha=1.0),
        "Elastic Net": ElasticNet(alpha=1.0, l1_ratio=0.5),
        "Polynomial (deg=2)": LinearRegression(),
    }

    r2_list = []
    rmse_list = []

    for name, m in compare_models.items():
        if "Polynomial" in name:
            poly = PolynomialFeatures(degree=2, include_bias=False)
            X_tr = poly.fit_transform(X_train)
            X_te = poly.transform(X_test)
        else:
            X_tr, X_te = X_train, X_test

        m.fit(X_tr, y_train)
        y_pred = m.predict(X_te)

        r2_list.append(r2_score(y_test, y_pred))
        rmse_list.append(np.sqrt(mean_squared_error(y_test, y_pred)))

    result_df = pd.DataFrame(
        {"모델": list(compare_models.keys()), "R² 점수": r2_list, "RMSE": rmse_list}
    )

    st.markdown("### 📋 모델별 성능 비교표")
    st.dataframe(result_df.style.background_gradient(cmap="YlGnBu", axis=0))

    # 시각화 (가로)
    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x="R² 점수", y="모델", data=result_df, palette="viridis", ax=ax)
        ax.set_title("모델별 R² 점수")
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x="RMSE", y="모델", data=result_df, palette="rocket", ax=ax)
        ax.set_title("모델별 RMSE")
        st.pyplot(fig)
