import streamlit as st
from sklearn.datasets import fetch_california_housing, load_breast_cancer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# 1. 데이터 선택
# -----------------------------
dataset_option = st.selectbox(
    "데이터셋을 선택하세요:",
    ("캘리포니아 집값 (California Housing)", "유방암 데이터 (Breast Cancer)"),
)

# -----------------------------
# 2. 데이터 로딩 및 제목 설정
# -----------------------------
if dataset_option == "캘리포니아 집값 (California Housing)":
    data = fetch_california_housing(as_frame=True)
    df = data.frame
    target_col = "MedHouseVal"
    title = "🏡 캘리포니아 주택 가격 예측 회귀 분석"
    description = "타겟: `MedHouseVal` (중간 주택 가격)"
else:
    data = load_breast_cancer(as_frame=True)
    df = data.frame
    df["target"] = data.target
    target_col = "target"
    title = "🧬 유방암 진단 회귀 분석"
    description = "타겟: `target` (0: 악성, 1: 양성)"

# -----------------------------
# 3. 제목 출력
# -----------------------------
st.title(title)
st.markdown(f"✅ **선택한 데이터**: {dataset_option}\n- {description}")

# -----------------------------
# 4. 회귀 분석 처리
# -----------------------------
X = df.drop(columns=[target_col])
y = df[target_col]

test_size = st.slider("검증 데이터 비율", 0.1, 0.5, 0.2)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=test_size, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# -----------------------------
# 5. 결과 출력
# -----------------------------
st.subheader("📊 회귀 성능 지표")
st.write(f"**R² score**: {r2_score(y_test, y_pred):.4f}")
st.write(f"**RMSE**: {mean_squared_error(y_test, y_pred, squared=False):.4f}")

# -----------------------------
# 6. 예측 vs 실제 시각화
# -----------------------------
st.subheader("📈 예측 결과 시각화")
fig, ax = plt.subplots()
sns.scatterplot(x=y_test, y=y_pred, ax=ax)
ax.set_xlabel("실제 값")
ax.set_ylabel("예측 값")
ax.set_title("실제 값 vs 예측 값")
st.pyplot(fig)

# -----------------------------
# 7. 회귀 계수
# -----------------------------
st.subheader("📌 회귀 계수")
coef_df = pd.DataFrame({"변수": X.columns, "회귀 계수": model.coef_}).sort_values(
    by="회귀 계수", key=abs, ascending=False
)
st.dataframe(coef_df)
