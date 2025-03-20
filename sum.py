import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

# Load environment variables
load_dotenv()  # This loads the .env file

# Get API Key
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Make sure it's set in the .env file!")

# Function to extract YouTube Video ID
def get_video_id(url_link):
    """Extracts video ID from a YouTube URL."""
    if "watch?v=" in url_link:
        return url_link.split("watch?v=")[-1]
    elif "youtu.be/" in url_link:
        return url_link.split("youtu.be/")[-1]
    return None

# Function to fetch transcript
def get_transcript(video_id):
    """Fetches transcript for the given video ID."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([line['text'] for line in transcript])
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None

# Function to generate response using Gemini AI
def generate_response(transcript_text):
    """Generates a response using Gemini AI."""
    if not transcript_text:
        return "No transcript available to generate response."

    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"Answer questions based on: \ntext = '{transcript_text}'"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {e}"

# Main Execution
if __name__ == "__main__":
    YOUTUBE_URL = "https://www.youtube.com/watch?v=0HoSwHNUOHg"

    video_id = get_video_id(YOUTUBE_URL)

    if video_id:
        transcript_text = get_transcript(video_id)
        response = generate_response(transcript_text)
        print(response)
    else:
        print("Invalid YouTube URL.")
