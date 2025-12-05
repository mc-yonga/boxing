import os
import time
import google.generativeai as genai
import yt_dlp
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
# Expects GOOGLE_API_KEY in environment variables
if "GOOGLE_API_KEY" in os.environ:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

def download_youtube_video(url, output_path="temp_video.mp4"):
    """
    Downloads a YouTube video using yt-dlp.
    Returns the path to the downloaded file or None if failed.
    """
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': output_path,
        'quiet': True,
        'no_warnings': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return output_path
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None

def upload_to_gemini(path, mime_type="video/mp4"):
    """
    Uploads the given file to Gemini.
    """
    try:
        file = genai.upload_file(path, mime_type=mime_type)
        print(f"Uploaded file '{file.display_name}' as: {file.uri}")
        return file
    except Exception as e:
        print(f"Error uploading to Gemini: {e}")
        return None

def wait_for_files_active(files):
    """
    Waits for the given files to be active.
    """
    print("Waiting for file processing...")
    for name in (file.name for file in files):
        file = genai.get_file(name)
        while file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(10)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"File {file.name} failed to process")
    print("...all files ready")

def analyze_video(file_uri):
    """
    Analyzes the video using Gemini 1.5 Pro.
    """
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config=generation_config,
    )

    prompt = """
    이 복싱 경기 영상을 분석해서 다음 내용을 작성해줘:
    1. 상대방의 주요 습관 (Habits)
    2. 공격 전조 동작 (Telegraphs)
    3. 방어적 헛점 (Weaknesses)
    4. 공략 팁
    """

    try:
        # Create the prompt parts with the file URI
        # Note: We can't pass the file object directly if we only have URI, 
        # but genai.GenerativeModel.generate_content can take the file object returned by upload_file
        # or we can retrieve it. 
        # Ideally, we pass the file object returned from upload_to_gemini.
        # But here we accept file_uri for simplicity if we were passing just URI strings, 
        # however the python library usually expects the file object or a specific part structure.
        # Let's assume the caller passes the file object or we fetch it.
        # Actually, let's change the signature to accept the file object for better safety, 
        # or just use the file object in the list.
        
        # For this implementation, let's assume we pass the file object or list of parts.
        # But to be safe with the prompt structure:
        response = model.generate_content([file_uri, prompt])
        return response.text
    except Exception as e:
        return f"Error during analysis: {e}"

def cleanup_file(path):
    """
    Removes the temporary file.
    """
    if os.path.exists(path):
        try:
            os.remove(path)
            print(f"Removed temporary file: {path}")
        except Exception as e:
            print(f"Error removing file: {e}")
