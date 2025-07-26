# #============================== IMPORTS ==============================

import streamlit as st
import os
import subprocess
from datetime import datetime
from TTS.api import TTS
from streamlit_lottie import st_lottie
# =====================================================================

# ============================ PAGE CONFIG ============================
st.set_page_config(page_title="AI Avatar Generator", layout="wide", page_icon="🧠")
# =====================================================================

# ========================= CUSTOM STYLING ============================
def local_css(css_text):
    st.markdown(f"<style>{css_text}</style>", unsafe_allow_html=True)

# CSS for cool background and glassmorphism
local_css("""
body {
    background: linear-gradient(135deg, #2c3e50, #3498db);
    font-family: 'Segoe UI', sans-serif;
    color: white;
}

section.main > div {
    backdrop-filter: blur(8px) saturate(120%);
    -webkit-backdrop-filter: blur(8px) saturate(120%);
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 30px;
    box-shadow: 0 8px 32px 0 rgba( 31, 38, 135, 0.37 );
}

.stButton>button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    border: none;
    color: white;
    font-weight: bold;
    padding: 0.7em 2em;
    border-radius: 30px;
    transition: all 0.3s ease-in-out;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #f7971e, #ffd200);
    transform: scale(1.05);
    cursor: pointer;
}
""")
# =====================================================================

# ========================== PAGE TITLE ===============================
st.markdown("<h1 style='text-align: center; color: white;'>🎭 AI Avatar Generator</h1>", unsafe_allow_html=True)
st.markdown("---")
# =====================================================================

# ========================== DEFINE PATHS =============================
source_image_dir = "examples/source_image"
driven_audio_dir = "examples/driven_audio"
result_dir = "results"
generated_audio_path = os.path.join(driven_audio_dir, "generated_audio.wav")
# =====================================================================

# ========================== MAIN LAYOUT ==============================
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🎨 Select Source Image")
    image_files = [f for f in os.listdir(source_image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    selected_image = st.selectbox("Choose a source image", image_files)

    if selected_image:
        st.image(os.path.join(source_image_dir, selected_image), caption="Selected Image Preview", width=200)

with col2:
    st.subheader("💬 Convert Text to Audio")
    user_text = st.text_area("Enter the text to convert into speech")

    if st.button("🔊 Generate Audio from Text"):
        if user_text.strip():
            with st.spinner("🔄 Synthesizing with VITS model..."):
                try:
                    tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=False)
                    speaker_id = "p226"
                    tts.tts_to_file(text=user_text, speaker=speaker_id, file_path=generated_audio_path)

                    st.success("✅ Audio generated and saved.")
                    st.audio(generated_audio_path)

                    with open(generated_audio_path, "rb") as file:
                        st.download_button(label="⬇ Download Audio (.wav)", data=file, file_name="avatar_audio.wav", mime="audio/wav")

                except Exception as e:
                    st.error(f"❌ TTS generation failed: {e}")
        else:
            st.warning("⚠ Please enter some text.")
# =====================================================================

# ========================== AUDIO SELECTION ==========================
st.markdown("---")
st.subheader("🎧 Select Driven Audio")

audio_files = [f for f in os.listdir(driven_audio_dir) if f.endswith('.wav')]

if "generated_audio.wav" in audio_files:
    audio_files.remove("generated_audio.wav")
    audio_files.insert(0, "generated_audio.wav")

selected_audio = st.selectbox("Choose a driven audio file", audio_files)
# =====================================================================

# ======================= AVATAR GENERATION BUTTON ====================
if "generate_clicked" not in st.session_state:
    st.session_state.generate_clicked = False

if st.button("✨ Generate Avatar"):
    st.session_state.generate_clicked = True
# =====================================================================

# ======================= RUN INFERENCE + DISPLAY VIDEO ===============
if st.session_state.generate_clicked:
    timestamp = datetime.now().strftime("%Y_%m_%d_%H.%M.%S")
    image_path = os.path.join(source_image_dir, selected_image)
    audio_path = os.path.join(driven_audio_dir, selected_audio)

    command = [
        "python", "inference.py",
        "--driven_audio", audio_path,
        "--source_image", image_path,
        "--result_dir", result_dir,
        "--still",
        "--preprocess", "full",
        "--enhancer", "gfpgan"
    ]

    with st.spinner("🛠 Generating video... Please wait..."):
        subprocess.run(command, shell=True)

    result_subdirs = [d for d in os.listdir(result_dir) if os.path.isdir(os.path.join(result_dir, d))]
    latest_dir = sorted(result_subdirs)[-1] if result_subdirs else None

    final_video = None
    if latest_dir:
        full_path = os.path.join(result_dir, latest_dir)
        video_files = [f for f in os.listdir(full_path) if f.endswith(".mp4")]
        if video_files:
            final_video = os.path.join(full_path, video_files[0])

    if final_video and os.path.exists(final_video):
        st.video(final_video)
        st.success("🎉 Done! Your talking avatar is ready.")
    else:
        st.error("❌ Couldn't find the generated video.")

    st.session_state.generate_clicked = False
