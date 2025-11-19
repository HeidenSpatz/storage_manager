import streamlit as st

# Configure for mobile/smartphone use
st.set_page_config(
    page_title="Storage Manager",
    page_icon="📱",
    layout="centered",  # Better for mobile screens
    initial_sidebar_state="collapsed",  # Sidebar collapsed by default on mobile
)

st.title("Hello, world!")

# Add celebration button
if st.button("🎉 Celebrate!"):
    st.balloons()
    st.success("Success! Keep up the great work!")
