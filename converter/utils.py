import cv2
import pytesseract
from gtts import gTTS
import os
# import os
import hashlib
import speech_recognition as sr
from pydub import AudioSegment
from django.conf import settings
from PIL import Image

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = os.path.join(settings.MEDIA_ROOT, "Tesseract-OCR", "tesseract.exe")
# pytesseract.pytesseract.tesseract_cmd = r"C:\msys64\mingw64\include\system\Project\braille_converter\tesseract.exe"
print(pytesseract.pytesseract.tesseract_cmd)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# if os.name == "nt":  # Windows
# else:  # Linux (Render)
#     pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
# TESSERACT_CMD = os.getenv("TESSERACT_PATH", "/usr/bin/tesseract")
# pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD
# import os


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
