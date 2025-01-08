import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.uix.spinner import Spinner
from googletrans import Translator
from gtts import gTTS
import os
from playsound import playsound
from kivy.uix.popup import Popup
from kivy.uix.label import Label

# Register custom fonts (use absolute path to fonts folder for all languages)

# Set the window size
Window.size = (360, 640)

# List of languages and their codes as per googletrans
languages = {
    'en': 'English',
    'hi': 'Hindi',
    'ml': 'Malayalam',
    'ta': 'Tamil',
    'bn': 'Bengali',
    'gu': 'Gujarati',
    'mr': 'Marathi',
    'pa': 'Punjabi',
    'kn': 'Kannada',
    'te': 'Telugu',
    'ur': 'Urdu',
    'ks': 'Kashmiri',
    'or': 'Odia'
}

# Reverse mapping for dropdown selection
lang_names_to_codes = {v: k for k, v in languages.items()}

class TranslatorApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Title Label
        self.title_label = Label(text="Translator & TTS App", font_size=24, size_hint=(1, 0.1), color=(0, 0, 0, 1), font_name="NotoSans")
        root.add_widget(self.title_label)

        # Input text area
        self.input_label = Label(text="Enter Text to Translate:", size_hint=(1, 0.05), font_name="NotoSans")
        root.add_widget(self.input_label)

        self.input_text = TextInput(hint_text="Type text here...", multiline=True, size_hint=(1, 0.2), height=200, font_size=18, font_name="NotoSans")
        root.add_widget(self.input_text)

        # Dropdown for source language
        self.source_lang_label = Label(text="Select Source Language:", size_hint=(1, 0.05), font_name="NotoSans")
        root.add_widget(self.source_lang_label)

        self.source_lang_spinner = Spinner(text='English', values=list(languages.values()), size_hint=(1, 0.1), height=50)
        root.add_widget(self.source_lang_spinner)

        # Dropdown for target language
        self.target_lang_label = Label(text="Select Target Language:", size_hint=(1, 0.05), font_name="NotoSans")
        root.add_widget(self.target_lang_label)

        self.target_lang_spinner = Spinner(text='Hindi', values=list(languages.values()), size_hint=(1, 0.1), height=50)
        root.add_widget(self.target_lang_spinner)

        # Translate Button
        self.translate_button = Button(text="Translate", size_hint=(1, 0.1), background_color=(0.2, 0.6, 1, 1))
        self.translate_button.bind(on_press=self.translate_text)
        root.add_widget(self.translate_button)

        # Output translated text area
        self.output_label = Label(text="Translated Text:", size_hint=(1, 0.05), font_name="NotoSans")
        root.add_widget(self.output_label)

        self.output_text = TextInput(hint_text="Translated text will appear here", multiline=True, size_hint=(1, 0.3), height=200, font_size=18, readonly=True, font_name="NotoSans")
        root.add_widget(self.output_text)

        # Copy Button
        self.copy_button = Button(text="Copy to Clipboard", size_hint=(1, 0.1), background_color=(0.2, 0.6, 1, 1))
        self.copy_button.bind(on_press=self.copy_text)
        root.add_widget(self.copy_button)

        # Play Audio Button
        self.play_audio_button = Button(text="Play Audio", size_hint=(1, 0.1), background_color=(0.2, 0.6, 1, 1))
        self.play_audio_button.bind(on_press=self.play_audio)
        root.add_widget(self.play_audio_button)

        return root

    def translate_text(self, instance):
        input_text = self.input_text.text.strip()

        if not input_text:
            self.show_popup("Input Error", "Please enter text to translate!")
            return

        source_lang = lang_names_to_codes.get(self.source_lang_spinner.text)
        target_lang = lang_names_to_codes.get(self.target_lang_spinner.text)

        if source_lang == target_lang:
            self.show_popup("Language Error", "Source and Target languages cannot be the same!")
            return

        translator = Translator()
        try:
            translated_text = translator.translate(input_text, src=source_lang, dest=target_lang).text
            self.output_text.text = translated_text
            self.text_to_speech(translated_text, target_lang)
        except Exception as e:
            self.show_popup("Translation Error", f"Error during translation: {str(e)}")

    def text_to_speech(self, translated_text, target_lang):
        try:
            tts = gTTS(text=translated_text, lang=target_lang)
            tts.save("translated_output.mp3")
            playsound("translated_output.mp3")
            os.remove("translated_output.mp3")
        except Exception as e:
            self.show_popup("TTS Error", f"Error during TTS: {str(e)}")

    def copy_text(self, instance):
        # Copy translated text to clipboard
        translated_text = self.output_text.text.strip()
        if translated_text:
            import pyperclip
            pyperclip.copy(translated_text)
            self.show_popup("Copied", "Translated text copied to clipboard!")
        else:
            self.show_popup("Copy Error", "No text to copy.")

    def play_audio(self, instance):
        # Play translated text audio again
        try:
            playsound("translated_output.mp3")
        except Exception as e:
            self.show_popup("Playback Error", f"Error during playback: {str(e)}")

    def show_popup(self, title, message):
        # Utility function to show popups
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()

# Run the app
if __name__ == "__main__":
    Translator
