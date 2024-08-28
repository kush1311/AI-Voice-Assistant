# AI Voice Assistant

## Overview
This project is an AI-powered Voice Assistant built using Python that listens to voice commands and performs various tasks such as answering questions, creating files, searching the web, playing music, and filling out online forms. The assistant leverages the Gemma2 model to answer a wide range of questions and uses a glowing visual indicator to reflect its listening and processing states, enhancing user engagement.

## Features
- **Advanced Question Answering**: Capable of answering a broad spectrum of questions using Gemma2.
- **Speech Recognition**: Captures voice commands using Google's Speech Recognition API.
- **Text-to-Speech**: Provides spoken responses using the pyttsx3 library.
- **Web Automation**: Automates tasks like web searches and music playback using Selenium WebDriver.
- **File Creation**: Creates text files based on voice commands.
- **Form Submission**: Automatically fills and submits forms on websites.
- **Visual Feedback**: A glowing circle on the GUI indicates the assistant's status (listening, processing).

## Requirements
- Python 3.10
- SpeechRecognition
- Pyttsx3
- Selenium
- Flask
- LangChain Community Package
- [Ollama](https://ollama.com) software for running Gemma2:2b
- ChromeDriver (compatible with your installed version of Chrome)

## Installation
1. **Install Ollama software:**
   - Download and install [Ollama](https://ollama.com).
   - Run the following command to download the Gemma2 model:
     ```bash
     ollama run Gemma2:2b
     ```

