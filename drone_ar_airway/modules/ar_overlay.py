import streamlit as st


def show_overlay(altitude):
    st.markdown(
        f"""
    <div style='position:absolute; top:10px; left:10px; background:#eee; padding: 10px; border-radius:8px;'>
        <h4>🛩️ 공중도로: 지도 클릭 기반 경로</h4>
        <b>고도:</b> {altitude}m<br>
        <b>경로 ID:</b> clicked-route
    </div>
    """,
        unsafe_allow_html=True,
    )
