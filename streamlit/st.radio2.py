import streamlit as st

genre = st.radio(
    "What's you favorite movie genre",
    [":rainbow[Comedy]", "***Drama***", "Documentary :movie_camera:"],
    captions=["Laugh out loud.", "Get the popcorn", "Never stop learning"],
)

if genre == ":rainbow[Comedy]":
    st.write("You selected comedy.")
else:
    st.write("You didn't select comedy.str")
