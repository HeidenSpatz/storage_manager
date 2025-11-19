import streamlit as st

st.title("Hello, world!")

# Add celebration button
if st.button("🎉 Celebrate!"):
    st.balloons()
    st.success("Success! Keep up the great work!")
