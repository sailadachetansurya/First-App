import streamlit as st
import os
import json
from streamlit_echarts import st_echarts

# Load your external CSS file
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

stories_dir = "stories"
story_folders = [f for f in os.listdir(stories_dir) if os.path.isdir(os.path.join(stories_dir, f))]

PROGRESS_FILE = "progress.json"

def save_progress():
    with open(PROGRESS_FILE, "w") as f:
        json.dump(st.session_state.unlocked_parts, f)

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {}

def load_markdown(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def donut_progress(percent):
    option = {
        "series": [
            {
                "type": "pie",
                "radius": ["70%", "90%"],
                "avoidLabelOverlap": False,
                "label": {"show": False},
                "labelLine": {"show": False},
                "data": [
                    {"value": percent, "name": "Completed", "itemStyle": {"color": "#00aaff"}},
                    {"value": 100 - percent, "name": "Remaining", "itemStyle": {"color": "#eee"}},
                ],
            }
        ]
    }
    st_echarts(option, height=100)  # smaller height here


st.title("📚 Interactive Story Hub")

# Initialize session state for story and unlocked parts
if "active_story" not in st.session_state:
    st.session_state.active_story = None

if "unlocked_parts" not in st.session_state:
    st.session_state.unlocked_parts = load_progress()

# ========== VIEW: STORY READER ==========
if st.session_state.active_story:
    story_id = st.session_state.active_story
    story_path = os.path.join(stories_dir, story_id)

    try:
        with open(os.path.join(story_path, "metadata.json"), "r", encoding="utf-8") as f:
            meta = json.load(f)
    except Exception as e:
        st.error(f"Failed to load story: {e}")
        st.stop()

    st.markdown(f"### 📖 {meta.get('title', story_id)}")
    st.caption(meta.get("description", ""))
    parts = meta["parts"]
    passwords = meta["passwords"]

    # Initialize unlocked state if needed
    if story_id not in st.session_state.unlocked_parts:
        st.session_state.unlocked_parts[story_id] = [0]

    # Show progress donut
    total_parts = len(parts)
    unlocked_count = len(st.session_state.unlocked_parts[story_id])
    progress_pct = unlocked_count / total_parts * 100
    st.markdown("### Your Progress")
    donut_progress(progress_pct)

    for i, part in enumerate(parts):
        if i in st.session_state.unlocked_parts[story_id]:
            content = load_markdown(os.path.join(story_path, part))
            st.markdown(content)

            if i + 1 < len(parts) and (i + 1) not in st.session_state.unlocked_parts[story_id]:
                with st.form(f"form_{story_id}_{i}"):
                    st.write(f"🔐 Enter password to unlock Part {i+2}:")
                    password_input = st.text_input("Password", type="password")
                    submitted = st.form_submit_button("Unlock")
                    if submitted:
                        if password_input == passwords[i + 1]:
                            st.success("✅ Correct! Unlocked next part.")
                            st.session_state.unlocked_parts[story_id].append(i + 1)
                            save_progress()
                            st.rerun()
                        else:
                            st.error("❌ Incorrect password.")
                break  # Show only one unlock form at a time

    st.markdown("---")
    if st.button("🔙 Back to story list"):
        st.session_state.active_story = None
        st.rerun()

# ========== VIEW: STORY SELECTION (Fancy Cards) ==========
else:
    st.markdown("<style>.stButton>button{width:100%;}</style>", unsafe_allow_html=True)  # make buttons full width inside cards
    
    # Layout cards in 2 columns (adjust as you want)
    cols = st.columns(2)
    for idx, folder in enumerate(story_folders):
        meta_path = os.path.join(stories_dir, folder, "metadata.json")
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
        except:
            continue
        
        col = cols[idx % 2]

        with col:
            # Create card container div with your CSS class "story-card"
            card_html = f"""
            <div class="story-card">
                <div class="story-card-title">{meta.get("title", folder)}</div>
                <div class="story-card-desc">{meta.get("description", "")}</div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)

            # Button below card
            if st.button("Read", key=folder):
                st.session_state.active_story = folder
                st.rerun()
