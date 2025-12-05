import streamlit as st
import os
import tempfile
from utils import download_youtube_video, upload_to_gemini, wait_for_files_active, analyze_video, cleanup_file

st.set_page_config(page_title="Boxing Match Analyst", page_icon="🥊", layout="wide")

st.title("🥊 Boxing Match Analyst")
st.markdown("Upload a video or provide a YouTube link to analyze boxing habits, telegraphs, and weaknesses.")

# Check for API Key
if "GOOGLE_API_KEY" not in os.environ:
    api_key = st.text_input("Enter your Google Gemini API Key", type="password")
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
        st.rerun()
    else:
        st.warning("Please enter your Google Gemini API Key to proceed.")
        st.stop()

# Tabs
tab1, tab2 = st.tabs(["📂 File Upload", "▶️ YouTube Link"])

with tab1:
    st.header("Upload Video File")
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi"])
    
    if uploaded_file is not None:
        st.video(uploaded_file)
        if st.button("Analyze Uploaded Video"):
            with st.spinner("Uploading and Analyzing..."):
                # Save uploaded file to temp
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = tmp_file.name
                
                try:
                    # Upload to Gemini
                    gemini_file = upload_to_gemini(tmp_path)
                    if gemini_file:
                        wait_for_files_active([gemini_file])
                        
                        # Analyze
                        result = analyze_video(gemini_file)
                        st.markdown("### 📊 Analysis Result")
                        st.markdown(result)
                        
                        # Cleanup Gemini file (optional, but good practice to mention)
                        # genai.delete_file(gemini_file.name)
                    else:
                        st.error("Failed to upload video to Gemini.")
                finally:
                    cleanup_file(tmp_path)

with tab2:
    st.header("YouTube Video Analysis")
    youtube_url = st.text_input("Enter YouTube URL")
    
    if youtube_url:
        if st.button("Analyze YouTube Video"):
            with st.spinner("Downloading, Uploading and Analyzing..."):
                # Download
                temp_video_path = "temp_yt_video.mp4"
                downloaded_path = download_youtube_video(youtube_url, temp_video_path)
                
                if downloaded_path:
                    st.success("Video downloaded successfully!")
                    # Optional: Show video? might be large or format issues, but let's try
                    # st.video(downloaded_path) 
                    
                    try:
                        # Upload to Gemini
                        gemini_file = upload_to_gemini(downloaded_path)
                        if gemini_file:
                            wait_for_files_active([gemini_file])
                            
                            # Analyze
                            result = analyze_video(gemini_file)
                            st.markdown("### 📊 Analysis Result")
                            st.markdown(result)
                        else:
                            st.error("Failed to upload video to Gemini.")
                    finally:
                        cleanup_file(downloaded_path)
                else:
                    st.error("Failed to download YouTube video. Please check the URL or try again.")
