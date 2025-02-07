import streamlit as st
import google.generativeai as genai
import google.ai.generativelanguage as glm
from PIL import Image
from gtts import gTTS
import base64

# Set API key
API_KEY = 'AIzaSyASPydGmQEx5L-JaAt1gpiAiddZGMm3cLQ'
genai.configure(api_key=API_KEY)

# Set page config
st.set_page_config(page_title="EduVox - Vision AI Learning Tool", page_icon="📚", layout="wide", initial_sidebar_state='collapsed')

# Custom CSS to style the page
st.markdown("""
    <style>
        body {
            background-color: #e6f7ff; /* Lighter shade of blue background */
            color: #333; /* Dark text color */
            font-family: Arial, sans-serif; /* Formal font */
            background-image: url('https://cdn.pixabay.com/photo/2015/10/22/02/08/books-1001629_960_720.jpg'); /* Background image of books */
            background-repeat: repeat; /* Repeat background image */
            background-size: cover; /* Cover the entire background */
        }
        .main-header {
            background-color: #00BFFF; /* Deep sky blue color */
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 42px;
            margin-bottom: 30px;
        }
        .upload-container {
            text-align: center;
            margin-bottom: 30px;
        }
        .generate-button {
            background-color: #87CEEB; /* Sky blue color */
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 18px;
            cursor: pointer;
            border-radius: 5px;
            margin-top: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Added box-shadow for button */
        }
        .generate-button:hover {
            background-color: #4682B4; /* Darker blue color */
        }
        .description {
            background-color: #E0FFFF; /* Light cyan background */
            padding: 20px;
            border-radius: 10px;
            margin-top: 30px;
            font-size: 18px;
            line-height: 1.6;
        }
        .credits {
            text-align: center;
            margin-top: 50px;
            font-size: 14px;
            color: #666;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">EduVox - Vision AI Learning Tool</div>', unsafe_allow_html=True)

# Function to generate audio and return HTML
def generate_audio_html(text):
    tts = gTTS(text=text, lang='en')
    audio_path = "output.mp3"
    tts.save(audio_path)
    with open(audio_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    audio_html = f"""
    <audio autoplay>
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
    </audio>
    """
    return audio_html

# File uploader and generate button
uploaded_file = st.file_uploader("🖼️ Upload an image", accept_multiple_files=False, type=['jpg', 'png'])
if uploaded_file is not None:
    st.image(uploaded_file, caption='📷 Uploaded Image', use_column_width=True)
    bytes_data = uploaded_file.getvalue()
    if st.button("🚀 Generate Description", key='generate_button', help="Click to generate a description and audio for the uploaded image") or uploaded_file is not None:
        try:
            # Create GenerativeModel and generate content
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(
                glm.Content(parts=[
                    glm.Part(text="👩‍🏫 You are a teacher. Please analyze the uploaded image and provide a detailed and descriptive explanation of its content as if you are teaching a visually impaired student. Describe all the key elements, objects, people, actions, and any notable features present in the image. Ensure the description is clear, concise, and easy to understand."),
                    glm.Part(inline_data=glm.Blob(mime_type='image/jpeg', data=bytes_data)),
                ]),
                stream=True
            )
            response.resolve()

            # Get description text
            description = response.text
            st.markdown(f'<div class="description">{description}</div>', unsafe_allow_html=True)

            # Generate and display audio
            audio_html = generate_audio_html(description)
            st.markdown(audio_html, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"An error occurred: {e}")

