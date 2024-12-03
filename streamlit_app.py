import streamlit as st
import requests
import os

# Configuration for cloud deployment
BACKEND_URL = "http://127.0.0.1:5000"  # Internal Docker communication

# Configure page
st.set_page_config(
    page_title="Photo Upload",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
    <style>
        .stButton>button {
            width: 100%;
            margin-top: 20px;
        }
        .upload-text {
            text-align: center;
            color: #666;
        }
        .main {
            padding: 2rem;
        }
        .stImage {
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)

st.title("📸 Photo Upload Service")

# Check backend health
try:
    response = requests.get(f"{BACKEND_URL}/health")
    if response.status_code == 200:
        st.success("✅ Backend service is running")
    else:
        st.error("❌ Backend service is not responding properly")
except:
    st.error("❌ Cannot connect to backend service")

# File uploader
uploaded_files = st.file_uploader(
    "Choose photos to upload",
    type=['png', 'jpg', 'jpeg', 'gif'],
    accept_multiple_files=True,
    help="Drag and drop your photos here"
)

if uploaded_files:
    st.write("### 📸 Preview")
    cols = st.columns(3)
    
    for idx, uploaded_file in enumerate(uploaded_files):
        with cols[idx % 3]:
            st.image(
                uploaded_file,
                caption=uploaded_file.name,
                use_column_width=True
            )
    
    if st.button('📤 Upload All Photos'):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        success_count = 0
        fail_count = 0
        total_files = len(uploaded_files)
        
        for idx, uploaded_file in enumerate(uploaded_files):
            status_text.text(f"Uploading {uploaded_file.name}...")
            progress = (idx + 1) / total_files
            progress_bar.progress(progress)
            
            try:
                files = {'file': (uploaded_file.name, uploaded_file.getvalue())}
                response = requests.post(f'{BACKEND_URL}/upload', files=files)
                
                if response.status_code == 200:
                    success_count += 1
                else:
                    fail_count += 1
                    st.error(f'❌ Failed to upload {uploaded_file.name}: {response.json().get("error", "Unknown error")}')
            except Exception as e:
                fail_count += 1
                st.error(f'❌ Error uploading {uploaded_file.name}: {str(e)}')
        
        progress_bar.empty()
        
        if success_count > 0:
            st.success(f'✅ Successfully uploaded {success_count} photo(s)!')
        if fail_count > 0:
            st.warning(f'⚠️ Failed to upload {fail_count} photo(s). Please try again.')

# Instructions
with st.expander("ℹ️ Instructions", expanded=False):
    st.markdown("""
        1. Click 'Browse files' or drag and drop photos
        2. Preview your photos in the grid view
        3. Click 'Upload All Photos' to start the upload
        
        **Supported formats:** PNG, JPG, JPEG, GIF  
        **Maximum file size:** 16MB per file
    """)
