import streamlit as st
import json
import os
from datetime import datetime
from PIL import Image

# --- Load Custom CSS ---
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Constants
MEMORY_FILE = "memories.json"
IMAGE_DIR = "memory_images"

# Ensure image folder exists
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# Load existing memories from JSON
def load_memories():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Save memory to JSON
def save_memory(memory):
    memories = load_memories()
    memories.append(memory)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memories, f, indent=2)

# 🔠 Page UI
st.markdown('<h1 class="animated">📝 Memory Wall</h1>', unsafe_allow_html=True)

name = st.text_input("🖋️ Your name or nickname")
memory_text = st.text_area("✨ Share a memory or message you'd like to leave")

emoji = st.selectbox("Pick a mood emoji", ["😊", "🥹", "💖", "🎉", "😄", "🌈", "✨", "🫶"])
uploaded_image = st.file_uploader("Optional: Upload a related image", type=["jpg", "jpeg", "png"])

if st.button("Post to Wall"):
    if name.strip() and memory_text.strip():
        image_filename = ""
        if uploaded_image:
            image_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uploaded_image.name}"
            image_path = os.path.join(IMAGE_DIR, image_filename)
            with open(image_path, "wb") as f:
                f.write(uploaded_image.getbuffer())

        memory = {
            "name": name.strip(),
            "message": memory_text.strip(),
            "emoji": emoji,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "image": image_filename
        }

        save_memory(memory)
        st.success("Memory posted! 💖")
    else:
        st.warning("Please enter both your name and a memory.")

# 📜 Display memories
st.subheader("🌟 Shared Memories")
memories = load_memories()

if memories:
    for m in reversed(memories):  # Show latest first
        st.markdown(f"""
            <div style="background-color:#fff9f0; padding:10px; margin-bottom:15px; border-radius:10px;">
                <b>{m['name']}</b> <span style="color:gray;">({m['timestamp']})</span><br>
                <span style="font-size:24px;">{m['emoji']}</span> <i>{m['message']}</i>
            </div>
        """, unsafe_allow_html=True)

        if m.get("image"):
            image_path = os.path.join(IMAGE_DIR, m["image"])
            if os.path.exists(image_path):
                st.image(image_path, use_column_width=True)
else:
    st.info("No memories yet. Be the first to leave a message! 💌")
