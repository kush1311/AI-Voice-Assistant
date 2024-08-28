import os
import speech_recognition as sr
import pyttsx3
from langchain_community.llms import Ollama
from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import threading

app = Flask(__name__)

# Initialize the speech recognizer and text-to-speech engine once
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)

# Lock for thread-safe text-to-speech operations
tts_lock = threading.Lock()

# Initialize Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
service = Service('chromedriver-win64/chromedriver.exe')  # Provide the path to chromedriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Initialize Ollama LLM (replace "gemma2:2b" with your preferred model)
ollama_llm = Ollama(model="gemma2:2b")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe_speech():
    try:
        with sr.Microphone() as source:
            status = "Listening... Speak now."
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=30)
            text = recognizer.recognize_google(audio)
            response = perform_manual_task(text)
            return jsonify({"status": status, "text": text, "response": response})
    except sr.UnknownValueError:
        return jsonify({"status": "Sorry, I could not understand the audio."})
    except sr.RequestError as e:
        return jsonify({"status": f"Could not request results; {e}"})

def perform_manual_task(text):
    if "open chrome" in text.lower():
        driver.get("https://www.google.com")
        return "Opened Chrome."
    elif "create file" in text.lower():
        with open("new_file.txt", "w") as file:
            file.write("This is a new file created by the voice command.")
        return "File created successfully."
    elif "play music" in text.lower() or "play song" in text.lower():
        driver.get("https://www.youtube.com/results?search_query=music")
        return "Searching for music on YouTube."
    elif "search for" in text.lower():
        search_query = text.lower().split("search for")[-1].strip()
        driver.get(f"https://www.google.com/search?q={search_query}")
        return f"Searching for {search_query} on Google."
    elif "fill form" in text.lower():
        driver.get("https://example.com/form")  # Replace with the actual URL
        try:
            input_field = driver.find_element_by_name("name")  # Replace with actual field name
            input_field.send_keys("Your Name")
            submit_button = driver.find_element_by_name("submit")  # Replace with actual submit button name
            submit_button.click()
            return "Form submitted successfully."
        except Exception as e:
            return f"Error in form submission: {e}"
    else:
        return generate_and_speak(text)

def generate_and_speak(text):
    if text:
        response = ollama_llm.invoke(text)
        try:
            # Use the lock to ensure thread-safe access to the TTS engine
            with tts_lock:
                engine.say(response)
                engine.runAndWait()
            return "Speaking: " + response
        except Exception as e:
            return f"Error in text-to-speech: {e}"
    return "No text to process."

if __name__ == '__main__':
    app.run(debug=True)
