import streamlit as st
import requests
import os

# Configuration for cloud deployment
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:5000')

st.set_page_config(page_title="Photo Upload", layout="wide")

st.title("Photo Upload Service")

# File uploader for multiple files
uploaded_files = st.file_uploader("Choose photos to upload", type=['png', 'jpg', 'jpeg', 'gif'], accept_multiple_files=True)

if uploaded_files:
    # Create columns for image preview
    cols = st.columns(3)  # Show 3 images per row
    
    for idx, uploaded_file in enumerate(uploaded_files):
        # Display the uploaded image in the appropriate column
        with cols[idx % 3]:
            st.image(uploaded_file, caption=f'Preview: {uploaded_file.name}', width=250)
    
    # Upload button
    if st.button('Upload All Photos'):
        with st.spinner('Uploading...'):
            success_count = 0
            fail_count = 0
            
            for uploaded_file in uploaded_files:
                # Prepare the file for upload
                files = {'file': (uploaded_file.name, uploaded_file.getvalue())}
                
                try:
                    # Send to Flask backend
                    response = requests.post(f'{BACKEND_URL}/upload', files=files)
                    
                    if response.status_code == 200:
                        success_count += 1
                    else:
                        fail_count += 1
                        st.error(f'Failed to upload {uploaded_file.name}: {response.json().get("error", "Unknown error")}')
                except requests.exceptions.ConnectionError:
                    fail_count += 1
                    st.error(f'Could not connect to the server while uploading {uploaded_file.name}')
            
            if success_count > 0:
                st.success(f'Successfully uploaded {success_count} photo(s)!')
            if fail_count > 0:
                st.warning(f'Failed to upload {fail_count} photo(s). Please try again.')

# Add some styling
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
    </style>
    """, unsafe_allow_html=True)

# Instructions
st.markdown("---")
st.markdown("""
    ### Instructions
    1. Click 'Browse files' to select multiple photos from your computer
    2. Preview your photos (arranged in a grid)
    3. Click 'Upload All Photos' to send them to your local storage
    
    Supported formats: PNG, JPG, JPEG, GIF
    Maximum file size: 16MB per file
""")
