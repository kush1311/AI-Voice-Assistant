import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
from langchain_community.llms import Ollama
import webbrowser
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Initialize the speech recognizer and text-to-speech engine once
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)

# Initialize Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
service = Service('chromedriver-win64/chromedriver.exe')  # Provide the path to chromedriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Function to handle speech recognition and update the circle color
def transcribe_speech():
    with sr.Microphone() as source:
        status_label.config(text="Listening... Speak now.")
        update_circle_color("red")
        window.update()
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=30)
            text = recognizer.recognize_google(audio)
            text_area.delete('1.0', tk.END)  # Clear previous text
            text_area.insert(tk.END, text)
            status_label.config(text="Transcription successful.")
            update_circle_color("blue")
            window.update()
            return text
        except sr.UnknownValueError:
            status_label.config(text="Sorry, I could not understand the audio.")
            update_circle_color("blue")
            return None
        except sr.RequestError as e:
            status_label.config(text=f"Could not request results; {e}")
            update_circle_color("blue")
            return None

# Function to update the circle's color
def update_circle_color(color):
    canvas.itemconfig(oval, outline=color)

def perform_manual_task(text):
    if "open chrome" in text.lower():
        driver.get("https://www.google.com")
    elif "create file" in text.lower():
        with open("new_file.txt", "w") as file:
            file.write("This is a new file created by the voice command.")
        status_label.config(text="File created successfully.")
    elif "play music" in text.lower() or "play song" in text.lower():
        driver.get("https://www.youtube.com/results?search_query=music")
    elif "search for" in text.lower():
        search_query = text.lower().split("search for")[-1].strip()
        driver.get(f"https://www.google.com/search?q={search_query}")
    elif "fill form" in text.lower():
        driver.get("https://example.com/form")  # Replace with the actual URL
        try:
            input_field = driver.find_element_by_name("name")  # Replace with actual field name
            input_field.send_keys("Your Name")
            submit_button = driver.find_element_by_name("submit")  # Replace with actual submit button name
            submit_button.click()
            status_label.config(text="Form submitted successfully.")
        except Exception as e:
            status_label.config(text=f"Error in form submission: {e}")
    else:
        generate_and_speak()

def generate_and_speak():
    text = text_area.get('1.0', tk.END).strip()
    if text:
        ollama_llm = Ollama(model="gemma2:2b")
        response = ollama_llm.invoke(text)
        try:
            engine.say(response)
            engine.runAndWait()
            status_label.config(text="Speaking...")
        except Exception as e:
            status_label.config(text=f"Error in text-to-speech: {e}")
    else:
        status_label.config(text="No text to process.")

def start_recognition():
    text = transcribe_speech()
    if text:
        perform_manual_task(text)

# Function to create a glowing effect
def animate_glow():
    while True:
        for i in range(15):
            color = f'#{hex(0x33 + i * 10)[2:]}{hex(0x33 + i * 10)[2:]}ff'
            canvas.itemconfig(oval, outline=color, width=5 + i)
            canvas.update()
            time.sleep(0.05)
        for i in range(15, 0, -1):
            color = f'#{hex(0x33 + i * 10)[2:]}{hex(0x33 + i * 10)[2:]}ff'
            canvas.itemconfig(oval, outline=color, width=5 + i)
            canvas.update()
            time.sleep(0.05)

# Set up the GUI window
window = tk.Tk()
window.title("Voice Assistant")
window.configure(bg='black')

# Create a canvas for the glowing effect
canvas = tk.Canvas(window, width=500, height=500, bg='black', highlightthickness=0)
canvas.pack()

# Create the glowing circle (oval)
oval = canvas.create_oval(150, 150, 350, 350, outline="blue", width=5)

# Start the glowing animation in a separate thread
glow_thread = threading.Thread(target=animate_glow)
glow_thread.daemon = True
glow_thread.start()

# Create GUI components
start_button = tk.Button(window, text="Start Speech Recognition", command=start_recognition)
start_button.pack(pady=10)

text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=60, height=10)
text_area.pack(pady=10)

status_label = tk.Label(window, text="Press 'Start Speech Recognition' to begin.", bg='black', fg='white')
status_label.pack(pady=10)

# Start the GUI event loop
window.mainloop()

# Close the Selenium WebDriver when the application exits
driver.quit()
