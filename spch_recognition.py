import speech_recognition as sr
from gtts import gTTS
import google.generativeai as genai
import os

# Configure the Google Generative AI API#
genai.configure(api_key="AIzaSyDRPY4FrWNUOqBPL6O-ZGcs3_5nsZ6gIvY")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
  ]
)

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source)  # Capture the audio input
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand you.")
            return "Sorry, I couldn't understand you."
        except sr.RequestError:
            print("Speech recognition service is unavailable.")
            return "Speech recognition service is unavailable."
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"

# Function: Get AI response from Google Generative AI
def get_ai_response(user_input):
    response = chat_session.send_message(user_input)
    return response

# Function: Convert text to speech
def text_to_speech(response_text):
    try:
        tts = gTTS(text=response_text, lang='en')
        tts.save("response.mp3")
        if os.name == 'nt':  # Windows
            os.system("start response.mp3")
        elif os.name == 'posix':  # macOS/Linux
            os.system("afplay response.mp3" if os.name == 'posix' else "xdg-open response.mp3")
    except Exception as e:
        print(f"Error during text-to-speech conversion: {e}")

# Main Workflow
def main():
    print("Welcome to the Voice Interaction System!")
    while True:
        try:
            user_text = speech_to_text()  # Get user input via speech-to-text
            if user_text.lower() in ["exit", "quit"]:
                print("Exiting the system. Goodbye!")
                break

            ai_response = get_ai_response(user_text)  # Get AI response
            print(f"AI Response: {ai_response.text}")
            text_to_speech(ai_response.text)  # Convert AI response to speech
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()


