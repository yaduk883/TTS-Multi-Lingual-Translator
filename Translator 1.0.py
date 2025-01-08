import tkinter as tk
from tkinter import messagebox
from googletrans import Translator
from gtts import gTTS
import os
from playsound import playsound
import pyperclip
import tkinter.simpledialog
from tkinter import font

# List of Indian and English languages and their codes as per googletrans
languages = {
    'en': 'English',
    'as': 'Assamese',
    'bn': 'Bengali',
    'gu': 'Gujarati',
    'hi': 'Hindi',
    'kn': 'Kannada',
    'ks': 'Kashmiri',
    'kok': 'Konkani',
    'mai': 'Maithili',
    'ml': 'Malayalam',
    'mr': 'Marathi',
    'ne': 'Nepali',
    'or': 'Odia',
    'pa': 'Punjabi',
    'sa': 'Sanskrit',
    'sat': 'Santali',
    'sd': 'Sindhi',
    'ta': 'Tamil',
    'te': 'Telugu',
    'ur': 'Urdu'
}

# Reverse the language dictionary to make it easier to use full language names in dropdown
lang_names_to_codes = {v: k for k, v in languages.items()}

# Font paths for different Indian languages
font_paths = {
    'Bengali': r'C:\Users\20hsm\PycharmProjects\pythonProject9\fonts\Noto_Sans_Bengali\NotoSansBengali-VariableFont_wdth,wght.ttf',
    'Devanagari': r'C:\Users\20hsm\PycharmProjects\pythonProject9\fonts\Noto_Sans_Devanagari\NotoSansDevanagari-VariableFont_wdth,wght.ttf',
    'Gujarati': r'C:\Users\20hsm\PycharmProjects\pythonProject9\fonts\Noto_Sans_Gujarati\NotoSansGujarati-VariableFont_wdth,wght.ttf',
    'Punjabi': r'C:\Users\20hsm\PycharmProjects\pythonProject9\fonts\Noto_Sans_Gurmukhi\NotoSansGurmukhi-VariableFont_wdth,wght.ttf',
    'Kannada': r'C:\Users\20hsm\PycharmProjects\pythonProject9\fonts\Noto_Sans_Kannada\NotoSansKannada-VariableFont_wdth,wght.ttf',
    'Malayalam': r'C:\Users\20hsm\PycharmProjects\pythonProject9\fonts\Noto_Sans_Malayalam\NotoSansMalayalam-VariableFont_wdth,wght.ttf',
    'Oriya': r'C:\Users\20hsm\PycharmProjects\pythonProject9\fonts\Noto_Sans_Oriya\NotoSansOriya-VariableFont_wdth,wght.ttf',
    'Tamil': r'C:\Users\20hsm\PycharmProjects\pythonProject9\fonts\Noto_Sans_Tamil\NotoSansTamil-VariableFont_wdth,wght.ttf',
    'Telugu': r'C:\Users\20hsm\PycharmProjects\pythonProject9\fonts\Noto_Sans_Telugu\NotoSansTelugu-VariableFont_wdth,wght.ttf'
}

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Translator & TTS")

        # Set up the GUI layout
        self.create_widgets()

        self.is_playing = False  # Flag to check if audio is playing
        self.tts_object = None  # Holds the TTS object for later playback
        self.audio_file = "translated_output.mp3"  # Audio file path

    def create_widgets(self):
        # Default font (this will be updated dynamically based on language selection)
        self.font = ('Arial', 12)

        # Input text section
        self.input_label = tk.Label(self.root, text="Enter Text to Translate:", font=self.font)
        self.input_label.pack(pady=5)

        # Input Text area (Text widget with scrollbar)
        self.input_text_frame = tk.Frame(self.root)
        self.input_text_frame.pack(pady=5)

        self.input_text = tk.Text(self.input_text_frame, width=50, height=5, wrap=tk.WORD, font=self.font)
        self.input_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar to the input text box
        self.scrollbar = tk.Scrollbar(self.input_text_frame, command=self.input_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.input_text.config(yscrollcommand=self.scrollbar.set)

        # Source language selection
        self.source_lang_label = tk.Label(self.root, text="Select Source Language:", font=self.font)
        self.source_lang_label.pack(pady=5)

        self.source_lang_var = tk.StringVar()
        self.source_lang_dropdown = tk.OptionMenu(self.root, self.source_lang_var, *languages.values())
        self.source_lang_dropdown.pack(pady=5)
        self.source_lang_var.set('English')  # Default to English

        # Target language selection
        self.target_lang_label = tk.Label(self.root, text="Select Target Language:", font=self.font)
        self.target_lang_label.pack(pady=5)

        self.target_lang_var = tk.StringVar()
        self.target_lang_dropdown = tk.OptionMenu(self.root, self.target_lang_var, *languages.values())
        self.target_lang_dropdown.pack(pady=5)
        self.target_lang_var.set('Hindi')  # Default to Hindi

        # Translate button
        self.translate_button = tk.Button(self.root, text="Translate", command=self.translate_text, font=self.font)
        self.translate_button.pack(pady=5)

        # Clear button to reset the text fields
        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_text, font=self.font)
        self.clear_button.pack(pady=5)

        # Translated text section (using Text widget for dynamic size)
        self.output_label = tk.Label(self.root, text="Translated Text:", font=self.font)
        self.output_label.pack(pady=5)

        self.output_text = tk.Text(self.root, width=50, height=5, wrap=tk.WORD, font=self.font)
        self.output_text.pack(pady=5)
        self.output_text.config(state=tk.DISABLED)  # Make it read-only initially

        # Copy button
        self.copy_button = tk.Button(self.root, text="Copy to Clipboard", command=self.copy_text, font=self.font)
        self.copy_button.pack(pady=5)

        # Play/Pause button for controlling audio playback
        self.play_button = tk.Button(self.root, text="Play", command=self.toggle_play, font=self.font)
        self.play_button.pack(pady=5)

        # Download button to save audio
        self.download_button = tk.Button(self.root, text="Download Audio", command=self.download_audio, font=self.font)
        self.download_button.pack(pady=5)

        # Exit button to quit the application
        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit, font=self.font)
        self.exit_button.pack(pady=10)

    def translate_text(self):
        # Get the input text
        input_text = self.input_text.get("1.0", tk.END).strip()
        if not input_text:
            messagebox.showwarning("Input Error", "Please enter some text to translate.")
            return

        # Get source and target languages from full names
        source_lang_name = self.source_lang_var.get()
        target_lang_name = self.target_lang_var.get()

        # Check if source and target languages are selected
        if source_lang_name == 'English' and target_lang_name == 'English':
            messagebox.showwarning("Language Error", "Please select a valid source and target language.")
            return

        # Check if source and target languages are the same
        if source_lang_name == target_lang_name:
            messagebox.showwarning("Language Error",
                                   "Source and Target languages cannot be the same. Please select different languages.")
            return

        # Convert full names to language codes
        source_lang_code = lang_names_to_codes.get(source_lang_name)
        target_lang_code = lang_names_to_codes.get(target_lang_name)

        # Before generating new audio, delete the previous audio file if it exists
        if os.path.exists(self.audio_file):
            os.remove(self.audio_file)

        # Translate the text using Google Translate API
        translator = Translator()
        translation = translator.translate(input_text, src=source_lang_code, dest=target_lang_code)

        # Get the translated text
        translated_text = translation.text
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)  # Clear any existing text
        self.output_text.insert(tk.END, translated_text)  # Insert the translated text
        self.output_text.config(state=tk.DISABLED)  # Make the output text readonly

        # Play the translated text using gTTS (Google Text-to-Speech)
        tts = gTTS(translated_text, lang=target_lang_code)
        tts.save(self.audio_file)
        self.tts_object = tts  # Store the TTS object for playback

        # Display message
        messagebox.showinfo("Translation Complete", "Translation and TTS audio are ready!")

        # Dynamically update the font for the translated text (change font based on language)
        if target_lang_name == "Bengali":
            self.update_font("Bengali")
        elif target_lang_name == "Hindi":
            self.update_font("Devanagari")
        elif target_lang_name == "Tamil":
            self.update_font("Tamil")
        elif target_lang_name == "Telugu":
            self.update_font("Telugu")
        else:
            self.update_font("Arial")  # Default font

    def update_font(self, language):
        # Use a custom font for different languages
        font_path = font_paths.get(language)
        if font_path and os.path.exists(font_path):
            # Load the font dynamically
            custom_font = font.Font(family=font_path, size=12)
            self.input_text.config(font=custom_font)
            self.output_text.config(font=custom_font)
        else:
            print(f"Font for {language} not found. Falling back to default.")

    def clear_text(self):
        # Clear the input and output text
        self.input_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)

    def copy_text(self):
        # Copy the translated text to the clipboard
        translated_text = self.output_text.get("1.0", tk.END).strip()
        if translated_text:
            pyperclip.copy(translated_text)
            messagebox.showinfo("Copied", "Translated text copied to clipboard.")

    def toggle_play(self):
        # Toggle audio playback (play or pause)
        if self.is_playing:
            messagebox.showinfo("Playback", "Audio is already playing.")
        else:
            playsound(self.audio_file)  # Play the sound file
            self.is_playing = True  # Set the flag to indicate audio is playing

    def download_audio(self):
        # Download the TTS audio to a file
        if self.tts_object:
            self.tts_object.save(self.audio_file)
            messagebox.showinfo("Download", f"Audio downloaded as {self.audio_file}")
        else:
            messagebox.showwarning("Error", "No audio to download.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()
