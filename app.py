import streamlit as st
from PIL import Image
import os

# Load logo
st.set_page_config(page_title="Ritavi Classes", layout="wide")
logo = Image.open("logo.png")
st.image(logo, width=200)

st.title("📘 Ritavi Classes - Maths & Science Materials")

# Sidebar filters
class_selected = st.sidebar.selectbox("Choose Class", ["6", "7", "8", "9", "10"])
subject = st.sidebar.selectbox("Choose Subject", ["Maths", "Science"])

# File display
folder = f"materials/Class_{class_selected}/{subject}"
os.makedirs(folder, exist_ok=True)

st.header(f"{subject} Materials - Class {class_selected}")

search = st.text_input("🔍 Search topics")

files = os.listdir(folder)
filtered_files = [f for f in files if search.lower() in f.lower()]

for file in filtered_files:
    if file.endswith(".pdf"):
        st.write(f"📄 {file}")
        with open(os.path.join(folder, file), "rb") as f:
            st.download_button("Download PDF", f, file_name=file)
    elif file.endswith((".mp4", ".webm")):
        st.video(os.path.join(folder, file))

# Upload (admin use only)
st.sidebar.markdown("### 📤 Upload Study Material")
uploaded_file = st.sidebar.file_uploader("Upload PDF or video", type=["pdf", "mp4", "webm"])
if uploaded_file:
    save_path = os.path.join(folder, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.read())
    st.sidebar.success("File uploaded successfully!")
