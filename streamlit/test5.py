import streamlit as st

st.markdown(
    """<div style='background-size : cover; padding:30px; text-align:center; color:white; border-radius:10px;'>
            <h2>Welcom to Streamlit</h2>
            <p style='font-size:18px;'>HTML과 CSS를 활용한 상단 배너</p>
            </div>
            
<table style="width:100%; margin-top:20px; border-collapse: collapse;"
border="1">
<tr style="background-color:#4CAF50; color:white;">
            <th>과목</th>
            <th>점수</th>
            </tr>
            <tr>
            <td>Python</td>
            <td>95</td>
            </tr>
            <tr>
            <td>HTML/CSS</td>
            <td>90</td>
            </tr>
            </table>
            """,
    unsafe_allow_html=True,
)
