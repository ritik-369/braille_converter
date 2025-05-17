import cv2
import pytesseract
from gtts import gTTS
import os
# import os
import hashlib
import speech_recognition as sr
from pydub import AudioSegment
from django.conf import settings
import requests
from PIL import Image
from tempfile import NamedTemporaryFile

# pytesseract.pytesseract.tesseract_cmd = os.path.join(settings.MEDIA_ROOT, "Tesseract-OCR", "tesseract.exe")
pytesseract.pytesseract.tesseract_cmd = os.path.join(settings.MEDIA_ROOT, "Tesseract-OCR", "tesseract.exe")
# pytesseract.pytesseract.tesseract_cmd = 'tesseract'


BRAILLE_MAP = {
    # Uppercase Letters
    "A": "⠁", "B": "⠃", "C": "⠉", "D": "⠙", "E": "⠑", "F": "⠋",
    "G": "⠛", "H": "⠓", "I": "⠊", "J": "⠚", "K": "⠅", "L": "⠇",
    "M": "⠍", "N": "⠝", "O": "⠕", "P": "⠏", "Q": "⠟", "R": "⠗",
    "S": "⠎", "T": "⠞", "U": "⠥", "V": "⠧", "W": "⠺", "X": "⠭",
    "Y": "⠽", "Z": "⠵",

    # Lowercase Letters (Braille requires capitalization prefix)
    "a": "⠁", "b": "⠃", "c": "⠉", "d": "⠙", "e": "⠑", "f": "⠋",
    "g": "⠛", "h": "⠓", "i": "⠊", "j": "⠚", "k": "⠅", "l": "⠇",
    "m": "⠍", "n": "⠝", "o": "⠕", "p": "⠏", "q": "⠟", "r": "⠗",
    "s": "⠎", "t": "⠞", "u": "⠥", "v": "⠧", "w": "⠺", "x": "⠭",
    "y": "⠽", "z": "⠵",

    # Numbers (Braille uses a number prefix)
    "0": "⠴", "1": "⠂", "2": "⠆", "3": "⠒", "4": "⠲",
    "5": "⠢", "6": "⠖", "7": "⠶", "8": "⠦", "9": "⠔",

    # Punctuation
    ".": "⠲", ",": "⠂", "?": "⠦", "!": "⠖", "-": "⠤",
    ":": "⠒", ";": "⠆", "(": "⠶", ")": "⠶", "/": "⠌",
    "'": "⠄", "\"": "⠘", "&": "⠯", "*": "⠡", "@": "⠈",
    "#": "⠼", "+": "⠖", "=": "⠶", "%": "⠩",

    # Space
    " ": " "
}


def text_to_braille(text):
    return ''.join(BRAILLE_MAP.get(char.upper(), char) for char in text)

def braille_to_text(braille):
    reverse_dict = {v: k for k, v in BRAILLE_MAP.items()}
    return ''.join(reverse_dict.get(char, '?') for char in braille)

def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        print(f"Extracted text from image: {text}")  # Debugging line
        return text.strip()
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""


def text_to_speech(text):
    if not text.strip():
        print("❌ Error: Empty text, skipping TTS.")
        return None

    try:
        audio_dir = os.path.join(settings.MEDIA_ROOT, 'audio_files')
        os.makedirs(audio_dir, exist_ok=True)
        audio_path = os.path.join(audio_dir, "audio_output.mp3")

        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(audio_path)

        print(f"✅ Audio saved: {audio_path} ({os.path.getsize(audio_path)} bytes)")

        return os.path.join('audio_files', 'audio_output.mp3')

    except Exception as e:
        print(f"❌ Error in text_to_speech: {e}")
        return None





    
def extract_text_from_audio(audio_path):
    """Extract text from audio file using speech recognition"""
    try:
        print(audio_path)
        recognizer = sr.Recognizer()
        
        # Handle different audio formats
        sound = AudioSegment.from_file(audio_path)
        with NamedTemporaryFile(suffix='.wav', delete=False) as tmp_wav:
            wav_path = tmp_wav.name
            sound.export(wav_path, format="wav")
        
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
        
        os.unlink(wav_path)
        return text
    
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""
    except Exception as e:
        print(f"Error processing audio: {e}")
        return ""


# .\venv\Scripts\Activate.ps1
