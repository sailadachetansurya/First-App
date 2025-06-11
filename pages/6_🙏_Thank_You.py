import streamlit as st # type: ignore

# --- Load Custom CSS ---
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.title("🙏 Thank You")

st.write("Thank you for sharing this space of love and celebration. May every day be filled with joy, affection, and cake! 🎂💖")
