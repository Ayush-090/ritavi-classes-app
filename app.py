import streamlit as st
import os

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_type = None

# Dummy credentials (replace with secure system or database)
ADMIN_PASSWORD = "admin123"

# Directory structure setup
BASE_DIR = "modules"
CLASSES = ["Class 9", "Class 10", "Class 11", "Class 12"]

for class_name in CLASSES:
    os.makedirs(os.path.join(BASE_DIR, class_name), exist_ok=True)

# Function to display logo
def display_logo():
    st.image("logo.png", width=200)  # Ensure you have a logo.png file in your project directory

# Function to create the login page
def login():
    st.title("Ritavi Classes Login")
    user_type = st.radio("Login as:", ["Student", "Admin"])
    password = st.text_input("Enter Password", type="password")
    
    if st.button("Login"):
        if user_type == "Admin" and password == ADMIN_PASSWORD:
            st.session_state.logged_in = True
            st.session_state.user_type = "admin"
        elif user_type == "Student":
            st.session_state.logged_in = True
            st.session_state.user_type = "student"
        else:
            st.error("Invalid credentials")

# Admin portal with added features
def admin_portal():
    display_logo()  # Display the logo
    
    st.title("Admin Portal - Ritavi Classes")

    menu = ["Upload Module", "Upload Timetable", "Upload Notes", "View Uploaded Content"]
    choice = st.selectbox("Choose an action", menu)
    
    if choice == "Upload Module":
        class_choice = st.selectbox("Select Class", CLASSES)
        uploaded_file = st.file_uploader("Upload PDF Module or Mock Test")
        if uploaded_file is not None:
            save_path = os.path.join(BASE_DIR, class_choice, uploaded_file.name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"Uploaded to {class_choice}")
    
    elif choice == "Upload Timetable":
        class_choice = st.selectbox("Select Class", CLASSES)
        timetable_file = st.file_uploader("Upload Timetable PDF or Image")
        if timetable_file is not None:
            save_path = os.path.join(BASE_DIR, class_choice, "Timetable", timetable_file.name)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, "wb") as f:
                f.write(timetable_file.getbuffer())
            st.success(f"Timetable uploaded to {class_choice}")
    
    elif choice == "Upload Notes":
        class_choice = st.selectbox("Select Class", CLASSES)
        notes_file = st.file_uploader("Upload Notes (PDF, Text, etc.)")
        if notes_file is not None:
            save_path = os.path.join(BASE_DIR, class_choice, "Notes", notes_file.name)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, "wb") as f:
                f.write(notes_file.getbuffer())
            st.success(f"Notes uploaded to {class_choice}")
    
    elif choice == "View Uploaded Content":
        class_choice = st.selectbox("Select Class", CLASSES)
        uploaded_files = os.listdir(os.path.join(BASE_DIR, class_choice))
        
        for file in uploaded_files:
            file_path = os.path.join(BASE_DIR, class_choice, file)
            st.write(f"### {file}")
            with open(file_path, "rb") as f:
                st.download_button("Download", f, file_name=file)

# Student portal for accessing content
def student_portal():
    st.title("Student Portal - Ritavi Classes")
    class_choice = st.selectbox("Select Your Class", CLASSES)
    files = os.listdir(os.path.join(BASE_DIR, class_choice))

    for file in files:
        file_path = os.path.join(BASE_DIR, class_choice, file)
        st.write(f"### {file}")
        with open(file_path, "rb") as f:
            st.download_button("Download", f, file_name=file)

# Main logic
if not st.session_state.logged_in:
    login()
else:
    if st.session_state.user_type == "admin":
        admin_portal()
    else:
        student_portal()
