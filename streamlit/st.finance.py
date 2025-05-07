import streamlit as st
import FinanceDataReader as fdr
import datetime
import plotly.graph_objects as go
import pandas as pd

# 한글 출력 시 Streamlit에서 UTF-8 자동 지원 (별도 sys 설정 제거)

st.set_page_config(page_title="📈 종목 코드 : 주가 차트 조회기")
st.title("📈 종목 코드 : 주가 차트 조회기")

# ===========================
# [1] 조회 시작일 입력
# ===========================
start_date = st.date_input("조회 시작일을 선택하세요", value=datetime.date(2022, 1, 1))

# ===========================
# [2] 종목코드 입력
# ===========================
stock_code = st.text_input(
    "종목 코드를 입력하세요 (예: 005930 = 삼성전자)", placeholder="6자리 숫자로 입력"
)

# ===========================
# [3] 차트 주기 선택
# ===========================
chart_type = st.selectbox("차트 주기를 선택하세요", options=["일봉", "주봉", "월봉"])

if stock_code and start_date:
    try:
        df = fdr.DataReader(stock_code, start=start_date)

        if df.empty:
            st.warning("❗ 해당 기간에 주가 데이터가 없습니다.")
        else:
            df.index = pd.to_datetime(df.index)

            # 주기변경
            if chart_type == "주봉":
                df = (
                    df.resample("W")
                    .agg(
                        {
                            "Open": "first",
                            "High": "max",
                            "Low": "min",
                            "Close": "last",
                            "Volume": "sum",
                        }
                    )
                    .dropna()
                )
            elif chart_type == "월봉":
                df = (
                    df.resample("M")
                    .agg(
                        {
                            "Open": "first",
                            "High": "max",
                            "Low": "min",
                            "Close": "last",
                            "Volume": "sum",
                        }
                    )
                    .dropna()
                )

            # 이동평균선 & 볼린저 밴드
            df["MA20"] = df["Close"].rolling(window=20).mean()
            df["Upper"] = df["MA20"] + df["Close"].rolling(window=20).std() * 2
            df["Lower"] = df["MA20"] - df["Close"].rolling(window=20).std() * 2

            # 캔들차트
            fig = go.Figure()

            fig.add_trace(
                go.Candlestick(
                    x=df.index,
                    open=df["Open"],
                    high=df["High"],
                    low=df["Low"],
                    close=df["Close"],
                    increasing_line_color="red",
                    decreasing_line_color="blue",
                    name="Candlestick",
                )
            )

            # 이동평균선 (MA20)
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["MA20"],
                    line=dict(color="orange", width=1.5),
                    name="MA20",
                )
            )

            # 볼린저 밴드
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["Upper"],
                    line=dict(color="gray", width=1, dash="dot"),
                    name="Bollinger Upper",
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["Lower"],
                    line=dict(color="gray", width=1, dash="dot"),
                    name="Bollinger Lower",
                )
            )

            fig.update_layout(
                title=f"{stock_code} - {chart_type} 캔들차트",
                xaxis_title="날짜",
                yaxis_title="가격",
                xaxis_rangeslider_visible=False,
            )

            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"데이터 로딩 중 오류 발생: {e}")
