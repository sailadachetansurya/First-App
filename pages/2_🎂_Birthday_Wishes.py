import streamlit as st
import time
import random

# --- Load Custom CSS ---
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# --- Persona Settings ---
personalities = {
    "princess": {
        "tone": "Romantic",
        "intro": "👑 Your Highness, today the stars shine for you.",
        "effect": st.balloons,
        "letter": """
### 👑 A Royal Celebration 👑
Princess, your presence graces this world like moonlight on a calm lake.  
May your every wish today be honored like a decree from the throne. 💖
""",
    },
    "vesper": {
        "tone": "Funny",
        "intro": "🎀 Vesper! Did you already sneak some cake? 🎂",
        "effect": st.snow,
        "letter": """
### 🌸 My Little Sunshine 🌸
Oh Vesper, the world gets brighter when you're around —  
like a sprinkle explosion in a candy shop! Never stop being adorably chaotic. 💕
""",
    },
    "madam ji": {
        "tone": "Heartfelt",
        "intro": "💼 Madam ji! A toast to your class and calm. 🍷",
        "effect": lambda: st.write("🥂 Cheers to elegance and intellect!"),
        "letter": """
### 💼 Wisdom Wrapped in Grace 💼
Madam ji, your poise, strength, and grace inspire me endlessly.  
Today is a tribute to your thoughtful soul and radiant presence. 🌟
""",
    },
    "sweetie": {
    "tone": "Sweet",
    "intro": "🍬 Buttercup! You're the softest hug in a hard world.",
    "effect": lambda: st.write("🌼 You're made of sugar and starlight."),
    "letter": """
    ### 🍭 Softest Soul 🍭  
    Buttercup, your sweetness melts my worries and fills my heart. 💗
    """
}

}

# --- Title ---
st.markdown('<h1 class="animated">🎂 Birthday Wishes & Love Letter Generator</h1>', unsafe_allow_html=True)

# --- Input ---
name = st.text_input("Whose birthday is it?")
st.caption("Princess? Vesper? Madam ji? Who is it today? 🧚‍♀️")

persona_key = name.lower().strip()
profile = personalities.get(persona_key)

# --- Persona Response ---
if profile:
    st.markdown(f"**{profile['intro']}**")
    profile["effect"]()
    default_tone = profile["tone"]
else:
    default_tone = "Sweet"

# --- Tone Selector ---
tone = st.selectbox("Tone of your wish", ["Sweet", "Funny", "Romantic", "Heartfelt"], index=["Sweet", "Funny", "Romantic", "Heartfelt"].index(default_tone))

# --- Generate Button ---
if st.button("Generate Wish"):
    st.markdown("⏳ Crafting the perfect message...")
    time.sleep(1.5)
    

    # --- Choose Wish by Tone ---
    if tone == "Funny":
        wish = f"{name}, you're not getting older... just more distinguished. Happy B-Day! 🎈"
    elif tone == "Romantic":
        wish = f"Happy Birthday, my love {name}. Every moment with you is a celebration. 💖"
    elif tone == "Heartfelt":
        wish = f"{name}, may your birthday be as wonderful and inspiring as you are. 🌟"
    else:
        wish = f"Happy Birthday, {name}! 🎉 Wishing you endless love, laughter, and joy."

    # --- Type-Out Effect ---
    placeholder = st.empty()
    typed = ""
    for char in wish:
        typed += char
        placeholder.markdown(f"**{typed}**")
        time.sleep(0.05)

    # --- Markdown Love Letter ---
    st.markdown("💌", unsafe_allow_html=True)
    time.sleep(0.5)

    if profile:
        st.markdown(profile["letter"])
    else:
        st.markdown(f"""
### 💖 My Love for {name} 💖

### 🎨 A Splash of Color in My Life 🎨
{name} is the **brightest rainbow** in my sky! 🌈✨

### ❤️ The Heartbeat of My World ❤️
Every moment with {name} fills me with **joy, warmth, and endless happiness**. 😊💫

### 🎶 A Symphony of Emotions 🎶
Life without {name} would be like music without melody. 🎵  
{name} makes everything **harmonious**! 🎼💕

### 💫 Forever Cherishing {name} 💫
> _{name} is a feeling, a universe, a forever-kind-of-love._ 💜✨
""")

# --- Optional Audio ---
try:
    audio_file = open("happy_birthday.mp3", "rb")
    st.audio(audio_file.read(), format="audio/mp3")
except FileNotFoundError:
    pass
