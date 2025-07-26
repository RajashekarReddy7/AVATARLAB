# AVATAR_LAB 🎭

An AI Avatar Generator Lab that creates realistic lip-synced talking avatars from a static image and an audio clip using GenAI models.

---

## 🚀 Features

- 🎤 Convert any audio into a lip-synced avatar video
- 🧠 Powered by VITS, SadTalker, GFPGAN, and face detection models
- 📦 Real-time video generation
- 🎨 Clean interface (Streamlit/Flask frontend)
- 🔒 Supports `.env` for environment config

---

## 🧰 Tech Stack

- **Backend:** Python, Flask
- **AI Models:** SadTalker, GFPGAN, Wav2Lip/VITS
- **Frontend:** Streamlit or HTML/CSS/JS (custom)
- **Other:** Torch, OpenCV, NumPy, FFmpeg

---

## 📁 Project Structure

AVATAR_LAB/
│
├── app.py # Main entry point
├── inference/ # Lip-sync & animation pipeline
├── checkpoints/ # Pretrained model weights (ignored in Git)
├── results/ # Output videos
├── static/ # Frontend assets
├── templates/ # HTML templates (if Flask)
├── requirements.txt # Python dependencies
└── README.md # You’re reading it!


---

## ⚙️ Setup Instructions
```bash
# Clone the repo
git clone https://github.com/RajashekarReddy7/AVATARLAB.git
cd AVATARLAB

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt

# Download models manually into checkpoints/
# (Follow SadTalker / VITS / GFPGAN model links)

# Run the app
python app.py
