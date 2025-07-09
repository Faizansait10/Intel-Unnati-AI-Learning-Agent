import os
import base64
from io import BytesIO
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv

# Google Cloud client libraries for STT and TTS
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech_v1beta1 as texttospeech
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# --- Authentication Setup ---
# This environment variable is picked up by Google Cloud client libraries
# for Speech-to-Text and Text-to-Speech using your service account key.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Configure Gemini API with the direct key and explicit endpoint
if os.getenv("GEMINI_API_KEY"):
    genai.configure(
        api_key=os.getenv("GEMINI_API_KEY"),
        # Explicitly set the API endpoint to ensure the correct version/location
        client_options={"api_endpoint": "generativelanguage.googleapis.com"}
    )
else:
    print("Warning: GEMINI_API_KEY not found in .env. Gemini API calls might fail.")
# --- End Authentication Setup ---

app = Flask(__name__, static_folder='../frontend', static_url_path='/')

# Initialize Google Cloud clients (outside of the route for efficiency)
speech_client = speech.SpeechClient()
texttospeech_client = texttospeech.TextToSpeechClient()

# Initialize Google Gemini Generative Model
try:
    # Using 'gemini-1.5-flash' model as confirmed to be working
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
    print("Gemini model initialized successfully with 'gemini-1.5-flash'.")
except Exception as e:
    print(f"Error initializing Gemini model: {e}")
    gemini_model = None # Set to None if initialization fails

# --- TEMPORARY CODE TO LIST AVAILABLE MODELS (commented out) ---
'''print("\n--- Listing Available Gemini Models ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Model Name: {m.name}, Supported Methods: {m.supported_generation_methods}")
except Exception as e:
    print(f"Error listing models: {e}")
'''
# --- END TEMPORARY CODE ---

# --- GLOBAL CHAT HISTORY (FOR DEMO PURPOSES) ---
# In a real application, you'd manage this per user, e.g., using Flask sessions or a database.
# Each entry is a dict: {'role': 'user'/'model', 'parts': [{'text': '...'}]}
chat_history = []
# --- END GLOBAL CHAT HISTORY ---


# --- Flask Routes to serve Frontend ---
@app.route('/')
def serve_index():
    # When the page is loaded, clear the chat history for a fresh start
    global chat_history
    chat_history = []
    print("Chat history cleared on page load.")
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# --- Speech-to-Text (STT) Function ---
def transcribe_audio(audio_data, sample_rate_hertz=48000, language_code="en-US"):
    """
    Transcribes audio data using Google Cloud Speech-to-Text.
    Args:
        audio_data (bytes): The raw audio content.
        sample_rate_hertz (int): The sample rate of the audio in Hertz.
        language_code (str): The language code (e.g., "en-US").
    Returns:
        str: The transcribed text or an error message.
    """
    audio = speech.RecognitionAudio(content=audio_data)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS, # Expects WebM/Opus from frontend
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=True, # Improves readability
    )
    try:
        response = speech_client.recognize(config=config, audio=audio)
        if response.results:
            return response.results[0].alternatives[0].transcript
        return "" # No transcription found
    except Exception as e:
        print(f"Error during speech recognition: {e}")
        return f"Error transcribing audio: {e}"

# --- Text-to-Speech (TTS) Function ---
def synthesize_speech(text, language_code="en-US", ssml_gender="NEUTRAL", voice_name="en-US-Standard-A"):
    """
    Synthesizes text into speech using Google Cloud Text-to-Speech.
    Args:
        text (str): The text to synthesize.
        language_code (str): The language code (e.g., "en-US").
        ssml_gender (str): The gender of the voice ("NEUTRAL", "MALE", "FEMALE").
        voice_name (str): The specific voice name (e.g., "en-US-Wavenet-C").
    Returns:
        bytes: The audio content bytes (MP3 format) or None if an error occurs.
    """
    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech.SsmlVoiceGender[ssml_gender],
        name=voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3 # Frontend expects MP3
    )

    try:
        response = texttospeech_client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        return response.audio_content # Returns bytes
    except Exception as e:
        print(f"Error during text-to-speech synthesis: {e}")
        return None

# --- Main Chat Endpoint ---
@app.route('/chat', methods=['POST'])
def chat():
    global chat_history # Declare chat_history as global to modify it

    user_text_input = request.form.get('text_input', '')
    audio_file = request.files.get('audio_input')

    full_user_query = user_text_input

    if audio_file:
        print("Received audio file.")
        try:
            audio_data = audio_file.read()
            transcribed_text = transcribe_audio(audio_data, sample_rate_hertz=48000)

            if transcribed_text.startswith("Error"):
                return jsonify({"response": transcribed_text, "audio_response_base64": ""}), 500

            if user_text_input:
                full_user_query = f"{user_text_input} (from audio: {transcribed_text})"
            else:
                full_user_query = transcribed_text

            print(f"Transcribed audio: {transcribed_text}")

        except Exception as e:
            print(f"Failed to process audio file: {e}")
            return jsonify({"response": f"Failed to process audio: {str(e)}", "audio_response_base64": ""}), 500

    if not full_user_query.strip():
        return jsonify({"response": "Please provide some input (text or audio).", "audio_response_base64": ""})

    # --- Add user query to chat history ---
    chat_history.append({'role': 'user', 'parts': [{'text': full_user_query}]})
    print(f"Current Chat History (after user): {chat_history}")

    # --- Integrate Gemini API ---
    bot_response_text = "I'm having trouble connecting to the AI model."
    if gemini_model:
        try:
            # Construct a system-like instruction for the model
            # This instruction will be prepended to the user's turn in the chat history
            # to guide Gemini's formatting without adding it to the persistent history.
            instruction = (
                "Please provide a detailed, point-wise explanation for the following. "
                "Ensure the response is well-structured using bullet points or numbered lists, "
                "and avoid unnecessary repetition. Focus on clarity and conciseness."
            )

            # The actual query sent to Gemini in the context of the history
            # The instructions are effectively part of the *current* user turn.
            query_for_gemini = f"{instruction}\n\nUser Query: {full_user_query}"

            print(f"Sending query to Gemini (with history): {query_for_gemini}")

            # Start a chat session with the full history
            # The last message in chat_history is the user's current query.
            # We are essentially sending the entire `chat_history` for context.
            chat_session = gemini_model.start_chat(history=chat_history)
            gemini_response = chat_session.send_message(query_for_gemini) # Send the formatted query

            bot_response_text = gemini_response.text
            print(f"Received response from Gemini: {bot_response_text}")

            # --- Add bot response to chat history ---
            chat_history.append({'role': 'model', 'parts': [{'text': bot_response_text}]})
            print(f"Current Chat History (after model): {chat_history}")

        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            bot_response_text = f"An error occurred with the AI model: {e}"
    else:
        print("Gemini model not initialized. Cannot generate AI response.")


    # Synthesize the bot's response into audio
    audio_response_bytes = synthesize_speech(bot_response_text)

    audio_base64 = ""
    if audio_response_bytes:
        audio_base64 = base64.b64encode(audio_response_bytes).decode('utf-8')
        print("Successfully synthesized audio response.")
    else:
        print("Failed to synthesize audio response.")

    return jsonify({
        "response": bot_response_text,
        "audio_response_base64": audio_base64
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)