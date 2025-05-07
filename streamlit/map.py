import streamlit as st
import pandas as pd
import numpy as np

# 서울 중심 좌표 : 위도 37.5665, 경도 126.9780 기준으로 난수 생성
df = pd.DataFrame(
    {
        "col1": np.random.randn(1000) / 200 + 37.5665,  # 위도 (좁게 분포)
        "col2": np.random.randn(1000) / 200 + 126.9780,  # 경도 (좁게 분포)
        "col3": np.abs(np.random.randn(1000)) * 50,  # size (절대값 사용)
        "col4": np.random.rand(1000, 4).tolist(),  # RGBA 색상
    }
)

# 지도 출력
st.map(df, latitude="col1", longitude="col2", size="col3", color="col4")
