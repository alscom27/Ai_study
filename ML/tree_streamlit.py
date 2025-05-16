import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import (
    load_iris,
    load_wine,
    load_diabetes,
    load_breast_cancer,
    fetch_california_housing,
)
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    mean_squared_error,
    r2_score,
    ConfusionMatrixDisplay,
)

from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, plot_tree
from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor,
    ExtraTreesClassifier,
    ExtraTreesRegressor,
    BaggingClassifier,
    BaggingRegressor,
    AdaBoostClassifier,
    AdaBoostRegressor,
    GradientBoostingClassifier,
    GradientBoostingRegressor,
    VotingClassifier,
)

# 한글 폰트 설정
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False


# ── 페이지 설정 ─────────────────────────────
st.set_page_config(
    page_title="👶 Beginner Model Explorer",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 사이드바: 설정 메뉴 ──────────────────────
st.sidebar.header("⚙️ Settings")

# 1) 데이터셋 고르기
DATASETS = {
    "Iris (분류)": load_iris,
    "Wine (분류)": load_wine,
    "Breast Cancer (분류)": load_breast_cancer,
    "Diabetes (회귀)": load_diabetes,
    # "House Price (회귀)": fetch_california_housing,
}
ds_name = st.sidebar.selectbox("1️⃣ 데이터셋 선택", list(DATASETS.keys()))
loader = DATASETS[ds_name]()
X, y = loader.data, loader.target
feature_names = loader.feature_names
target_names = getattr(loader, "target_names", None)
is_reg = "회귀" in ds_name

# 2) 모델 고르기
st.sidebar.markdown("2️⃣ 모델 선택")
ALL_MODELS = {
    "KNN": (KNeighborsRegressor if is_reg else KNeighborsClassifier),
    "SVR": (SVR if is_reg else SVR),
    "Decision Tree": (DecisionTreeRegressor if is_reg else DecisionTreeClassifier),
    "Random Forest": (RandomForestRegressor if is_reg else RandomForestClassifier),
    "Extra Trees": (ExtraTreesRegressor if is_reg else ExtraTreesClassifier),
    "Bagging": (BaggingRegressor if is_reg else BaggingClassifier),
    "AdaBoost": (AdaBoostRegressor if is_reg else AdaBoostClassifier),
    "Gradient Boosting": (
        GradientBoostingRegressor if is_reg else GradientBoostingClassifier
    ),
}
if not is_reg:
    ALL_MODELS["Voting"] = VotingClassifier(
        [
            ("rf", RandomForestClassifier()),
            ("et", ExtraTreesClassifier()),
            ("dt", DecisionTreeClassifier()),
        ],
        voting="hard",
    )
models = st.sidebar.multiselect(
    "비교할 모델 (최소 1개)",
    list(ALL_MODELS.keys()),
    default=list(ALL_MODELS.keys())[:3],
)

# 3) 정렬 기준
st.sidebar.markdown("3️⃣ 결과 정렬")
sort_by = st.sidebar.selectbox("정렬 기준", ["Test Score", "Train Score"])
asc = st.sidebar.radio("오름/내림차순", ["내림차순", "오름차순"]) == "오름차순"

# 4) 실행 버튼
run = st.sidebar.button("▶️ 실행")

# ── 메인 화면 ───────────────────────────────
st.title("👶 Beginner Model Explorer")
st.write("**단계별로 따라가며 모델 성능을 직관적으로 비교해보세요!**")

# ── Step 1: 데이터 보기 ─────────────────────
with st.expander("🔍 Step 1. 데이터 미리 보기"):
    st.write(f"- **데이터셋**: `{ds_name}`")
    st.write(f"- **샘플 수**: {X.shape[0]}개, **특징 수**: {X.shape[1]}개")
    df = pd.DataFrame(X, columns=feature_names)
    if target_names is not None:
        df["Target"] = [target_names[i] for i in y]
    else:
        df["Target"] = y
    st.dataframe(df.head(), use_container_width=True)

# 실행을 누른 뒤 아래부터 결과가 나옵니다.
if run and models:
    # ── Step 2: Cross-Validation ──────────────
    st.markdown("## 2️⃣ Cross-Validation 결과 모으기")
    scoring = "r2" if is_reg else "accuracy"
    results_avg = {}
    results_raw = {}

    for name in models:
        Cls = ALL_MODELS[name]
        clf = Cls() if name != "Voting" else ALL_MODELS["Voting"]
        pipe = make_pipeline(StandardScaler(), clf)
        cv = cross_validate(pipe, X, y, cv=5, scoring=scoring, return_train_score=True)
        results_avg[name] = {
            "Test Score": cv["test_score"].mean(),
            "Train Score": cv["train_score"].mean(),
        }
        results_raw[name] = cv["test_score"]

    df_avg = pd.DataFrame(results_avg).T
    df_avg["Std Dev"] = pd.Series({m: np.std(results_raw[m]) for m in models})
    df_avg = df_avg.sort_values(by=sort_by, ascending=asc)

    # ── Step 3: 컬러 테이블 ───────────────────
    st.markdown("## 3️⃣ 평균 성능 컬러 테이블")
    st.dataframe(
        df_avg.style.background_gradient(subset=["Test Score"], cmap="Blues").format(
            "{:.4f}"
        ),
        use_container_width=True,
    )

    # ── Step 4: Error Bar 그래프 ──────────────
    st.markdown("## 4️⃣ 에러바 차트로 비교하기")
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.bar(df_avg.index, df_avg["Test Score"], yerr=df_avg["Std Dev"], capsize=5)
    ax.set_ylabel(scoring.upper())
    ax.set_title("평균 Test Score ± 표준편차")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

    # ── Step 5: Fold별 Boxplot ───────────────
    st.markdown("## 5️⃣ Fold별 분포 확인")
    fig2, ax2 = plt.subplots(figsize=(6, len(models) * 0.4))
    ax2.boxplot(
        [results_raw[m] for m in df_avg.index], labels=df_avg.index, notch=False
    )
    ax2.set_ylabel(scoring.upper())
    ax2.set_title("5-Fold Test Score 분포")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig2)

    # ── Step 6: 회귀 vs 분류 별 추가 시각화 ───
    if is_reg:
        st.markdown("## 6️⃣ 회귀: 예측 vs 실제 산점도")
        X_tr, X_te, y_tr, y_te = train_test_split(
            StandardScaler().fit_transform(X), y, test_size=0.3, random_state=42
        )
        for name in df_avg.index:
            if name == "Voting":
                continue
            model = ALL_MODELS[name]().fit(X_tr, y_tr)
            y_pr = model.predict(X_te)
            fig3, ax3 = plt.subplots(figsize=(4, 3))
            ax3.scatter(y_te, y_pr, alpha=0.5)
            m, b = np.polyfit(y_te, y_pr, 1)
            ax3.plot(y_te, m * y_te + b, color="red")
            ax3.set_title(name)
            ax3.set_xlabel("실제 값")
            ax3.set_ylabel("예측 값")
            st.pyplot(fig3)

    else:
        st.markdown("## 6️⃣ 분류: 최상위 모델 혼동 행렬")
        # ▶ train/test split 결과를 4개 변수로 분리
        X_tr, X_te, y_tr, y_te = train_test_split(
            StandardScaler().fit_transform(X), y, test_size=0.3, random_state=42
        )
        best = df_avg.index[0]
        model = ALL_MODELS[best]().fit(X_tr, y_tr)

        fig4, ax4 = plt.subplots()
        ConfusionMatrixDisplay.from_estimator(
            model, X_te, y_te, display_labels=target_names, ax=ax4
        )
        ax4.set_title(f"{best} 혼동 행렬")
        st.pyplot(fig4)
