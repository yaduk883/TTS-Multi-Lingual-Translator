from flask import Flask, render_template, request, jsonify
from googletrans import Translator
from gtts import gTTS
import os
import speech_recognition as sr

# Initialize the Flask app
app = Flask(
    __name__,
    template_folder="templates",  # Specify the correct template folder
    static_folder="static"  # Specify the folder for static files like CSS, JS, images
)

# Initialize the Google Translator
translator = Translator()

@app.route('/')
def index():
    """
    Render the main index.html file located in the templates folder.
    """
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_text():
    """
    Translate text from the source language to the target language
    and generate TTS for the translated text.
    """
    text = request.form.get('text')
    source_lang = request.form.get('source_lang')
    target_lang = request.form.get('target_lang')

    try:
        # Perform the translation
        result = translator.translate(text, src=source_lang, dest=target_lang)
        translated_text = result.text

        # Save the translated text as an audio file
        audio_file = os.path.join(app.static_folder, "translated_output.mp3")
        tts = gTTS(translated_text, lang=target_lang)
        tts.save(audio_file)

        return jsonify({"translated_text": translated_text, "audio_file": "static/translated_output.mp3"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    """
    Convert speech input from the microphone to text.
    """
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source)

        # Convert speech to text using Google Speech Recognition
        text = recognizer.recognize_google(audio)
        return jsonify({"speech_text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the app in debug mode for development purposes
    app.run(debug=True)
