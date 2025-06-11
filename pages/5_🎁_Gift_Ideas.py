import streamlit as st # type: ignore
import random
import time

# --- Load Custom CSS ---
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.title("🎁 Gift Ideas")

quotes = [
    "Love is not about how many days, months, or years you have been together. It's about how much you love each other every single day.",
    "You are the poem I never knew how to write, and this life is the story I’ve always wanted to tell.",
    "In your smile, I see something more beautiful than the stars.",
]

st.markdown("""
Here are some thoughtful gift ideas:
- 🌸 Personalized photo book
- 💌 Handwritten love letter
- 🎧 Romantic playlist of your sweet voice
- 🧁 DIY craft box
""")

preqe = [ 
        "✨ Thinking of something sweet...",
        "Chanelling the inner shakespeare... "
        
    ]

if st.button("Surprise Me"):
    st.write(random.choice(preqe))
    time.sleep(2)
    st.success(random.choice(quotes))

st.snow()  # Creates snow effect
