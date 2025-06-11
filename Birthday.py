import streamlit as st # type: ignore
from PIL import Image # type: ignore  # noqa: F401

st.set_page_config(page_title="Love & Birthday Celebration", page_icon="🎉", layout="centered")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("💖 Welcome to the Love & Birthday Celebration! 🎂")

st.markdown("""
Welcome to a special place crafted with love and joy!  
Explore heartfelt quotes, share memories, browse sweet gift ideas, and celebrate the magic of love and birthdays.  
""")

# image = Image.open("birthday_love_banner.jpg")  # Optional banner image
# st.image(image, use_column_width=True)
