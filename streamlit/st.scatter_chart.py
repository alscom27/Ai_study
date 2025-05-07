import streamlit as st
import pandas as pd
import numpy as np

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["col1", "col2", "col3"])

chart_data["col4"] = np.random.choice(["A", "B", "C"], 20)

st.scatter_chart(chart_data, x="col1", y="col2", color="col4", size="col3")
