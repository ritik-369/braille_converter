from django.shortcuts import render
from .forms import *
from .utils import *
from .models import *
from django.contrib.auth.decorators import login_required
import os
from typing import Optional
import tempfile
from django.conf import settings
import logging
from django.core.files.storage import FileSystemStorage
from tempfile import NamedTemporaryFile
import base64
from datetime import datetime
import wave
import requests
import speech_recognition as sr
from pydub import AudioSegment
from .forms import ChatBotQueryForm
import django
import sys
from .models import ChatBotQuery


logger = logging.getLogger(__name__)

@login_required
def menu_view(request):
    return render(request, 'converter/menu.html')
def text_to_braille_view(request):
    form = BrailleTextForm()
    braille = None
    if request.method == 'POST':
        form = BrailleTextForm(request.POST)
        if form.is_valid():
            braille = text_to_braille(form.cleaned_data['text'])
    return render(request, 'converter/text_to_braille.html', {'form': form, 'braille': braille})

def braille_to_text_view(request):
    form = BrailleTextForm()
    text = None
    if request.method == 'POST':
        form = BrailleTextForm(request.POST)
        if form.is_valid():
            text = braille_to_text(form.cleaned_data['text'])
    return render(request, 'converter/braille_to_text.html', {'form': form, 'text': text})

def image_to_braille_view(request):
    form = ImageUploadForm()
    braille_text = None

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            extracted_text = extract_text_from_image(instance.image.path)

            print(f"Extracted Text: {extracted_text}")  # Debugging

            if extracted_text.strip():
                braille_text = text_to_braille(extracted_text)  # Convert text to Braille
            else:
                return render(request, 'converter/image_to_braille.html',
                              {'form': form, 'error': 'No text extracted from the image.'})

    return render(request, 'converter/image_to_braille.html', {'form': form, 'braille': braille_text})


def image_to_audio_view(request):
    form = ImageUploadForm()
    audio_file = None
    
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            extracted_text = extract_text_from_image(instance.image.path)

            if not extracted_text.strip():
                return render(request, 'converter/image_to_audio.html', 
                              {'form': form, 'error': 'Failed to extract text from image.'})

            audio_file = text_to_speech(extracted_text)

            print(f"Extracted text: {extracted_text}")  # Debugging line

            if not audio_file:
                return render(request, 'converter/image_to_audio.html', 
                              {'form': form, 'error': 'Failed to generate audio.'})

    return render(request, 'converter/image_to_audio.html', {'form': form, 'audio_file': audio_file,'MEDIA_URL': settings.MEDIA_URL})



def chatbot_view(request):
    form = ChatBotQueryForm()
    response_data = {}
    
    if request.method == 'POST':
        form = ChatBotQueryForm(request.POST, request.FILES)
        
        if form.is_valid():
            chat_query = form.save(commit=False)
            chat_query.user = request.user
            
            # Handle different input types
            input_type = form.cleaned_data['input_type']
            output_type = form.cleaned_data['output_type']
            
            # Process input
            text_input = ""
            if input_type == 'text':
                text_input = form.cleaned_data['text_input']
            elif input_type == 'audio_file':
                
                print(request.FILES['audio_input'])
                audio_file = request.FILES['audio_input']
        
                # with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                #     temp_file.write(audio_file.read())
                #     temp_file_path = temp_file.name
                # text_input = extract_text_from_audio(audio_file.temporary_file_path())
                fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'temp'))
                temp_name = fs.save(audio_file.name, audio_file)
                temp_path = fs.path(temp_name)
                
                recognizer = sr.Recognizer()
                file_extension = os.path.splitext(temp_path)[1].lower()
                
                if file_extension == '.wav':
                    with sr.AudioFile(temp_path) as source:
                        audio_data = recognizer.record(source)
                        extracted_text = recognizer.recognize_google(audio_data)
                else:
                    sound = AudioSegment.from_file(temp_path)
                    with NamedTemporaryFile(suffix='.wav', delete=False) as tmp_wav:
                        wav_path = tmp_wav.name
                        sound.export(wav_path, format="wav")
                    
                    with sr.AudioFile(wav_path) as source:
                        audio_data = recognizer.record(source)
                        extracted_text = recognizer.recognize_google(audio_data)
                    
                    os.unlink(wav_path)
                
                fs.delete(temp_name)
                text_input=extracted_text
                print(text_input)
                
            elif input_type == 'recording':
                audio_data = request.POST.get('audio_data')
                if not audio_data:
                    raise ValueError("No audio data received")
                
                # Remove data URL prefix if present
                if ',' in audio_data:
                    audio_data = audio_data.split(',')[1]
                
                # Convert base64 to bytes
                audio_bytes = base64.b64decode(audio_data)
                
                # Create audio_files directory if it doesn't exist
                audio_dir = os.path.join(settings.MEDIA_ROOT, 'audio_files')
                os.makedirs(audio_dir, exist_ok=True)
                
                # Generate unique filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                mp3_filename = f"recording_{timestamp}.mp3"
                mp3_path = os.path.join(audio_dir, mp3_filename)
                
                # First save as MP3
                with open(mp3_path, 'wb') as mp3_file:
                    mp3_file.write(audio_bytes)
                
                # Now process the MP3 file
                sound = AudioSegment.from_file(mp3_path)
                with NamedTemporaryFile(suffix='.wav', delete=False) as tmp_wav:
                    wav_path = tmp_wav.name
                    sound.set_frame_rate(16000).set_channels(1).export(
                        wav_path, 
                        format="wav",
                        codec="pcm_s16le"
                    )
                
                # Process the converted WAV file
                recognizer = sr.Recognizer()
                try:
                    with sr.AudioFile(wav_path) as source:
                        audio_data = recognizer.record(source)
                        extracted_text = recognizer.recognize_google(audio_data)

                except Exception as e:
                    raise Exception(f"Recognition failed. Original audio saved at {mp3_path}. Error: {str(e)}")
                finally:
                    # Clean up temporary WAV file
                    os.unlink(wav_path)
                text_input=extracted_text

            
            if not text_input:
                return render(request, 'converter/chatbot.html', {
                    'form': form,
                    'error': 'Could not process input. Please try again.'
                })
            
            chat_query.text_input = text_input
            
            # Get LLM response
            llm_response = get_llm_response(text_input)
            chat_query.llm_response = llm_response
            
            # Process output based on selected type
            if output_type == 'braille':
                chat_query.braille_response = text_to_braille(llm_response)

            elif output_type == 'audio':
                audio_file = text_to_speech(llm_response)
                
                if audio_file:
                    chat_query.audio_response = audio_file
            
            chat_query.save()
            
            # Prepare response data
            response_data = {
                'input_text': text_input,
                'llm_response': llm_response,
                'output_type': output_type,
            }
            
            if output_type == 'braille':
                response_data['braille_response'] = chat_query.braille_response
            elif output_type == 'audio':
                response_data['audio_response'] = chat_query.audio_response.url if chat_query.audio_response else None

            # Reset form for new queries
            form = ChatBotQueryForm()
    
    return render(request, 'converter/chatbot.html', {
        'form': form,
        'response_data': response_data,
        'MEDIA_URL': settings.MEDIA_URL,
    })

def audio_to_braille_view(request):
    form = AudioUploadForm()
    braille_text = None
    extracted_text = None
    
    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES)
        audio_source = request.POST.get('audio_source', 'upload')
        
        try:
            if audio_source == 'upload' and form.is_valid():
                # Handle file upload (existing code remains the same)
                audio_file = request.FILES['audio_file']
                
                fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'temp'))
                temp_name = fs.save(audio_file.name, audio_file)
                temp_path = fs.path(temp_name)
                
                recognizer = sr.Recognizer()
                file_extension = os.path.splitext(temp_path)[1].lower()
                
                if file_extension == '.wav':
                    with sr.AudioFile(temp_path) as source:
                        audio_data = recognizer.record(source)
                        extracted_text = recognizer.recognize_google(audio_data)
                else:
                    sound = AudioSegment.from_file(temp_path)
                    with NamedTemporaryFile(suffix='.wav', delete=False) as tmp_wav:
                        wav_path = tmp_wav.name
                        sound.export(wav_path, format="wav")
                    
                    with sr.AudioFile(wav_path) as source:
                        audio_data = recognizer.record(source)
                        extracted_text = recognizer.recognize_google(audio_data)
                    
                    os.unlink(wav_path)
                
                fs.delete(temp_name)
                
            elif audio_source == 'record':
                # Handle recorded audio (base64)
                audio_data = request.POST.get('audio_data')
                if not audio_data:
                    raise ValueError("No audio data received")
                
                # Remove data URL prefix if present
                if ',' in audio_data:
                    audio_data = audio_data.split(',')[1]
                
                # Convert base64 to bytes
                audio_bytes = base64.b64decode(audio_data)
                
                # Create audio_files directory if it doesn't exist
                audio_dir = os.path.join(settings.MEDIA_ROOT, 'audio_files')
                os.makedirs(audio_dir, exist_ok=True)
                
                # Generate unique filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                mp3_filename = f"recording_{timestamp}.mp3"
                mp3_path = os.path.join(audio_dir, mp3_filename)
                
                # First save as MP3
                with open(mp3_path, 'wb') as mp3_file:
                    mp3_file.write(audio_bytes)
                
                # Now process the MP3 file
                sound = AudioSegment.from_file(mp3_path)
                with NamedTemporaryFile(suffix='.wav', delete=False) as tmp_wav:
                    wav_path = tmp_wav.name
                    sound.set_frame_rate(16000).set_channels(1).export(
                        wav_path, 
                        format="wav",
                        codec="pcm_s16le"
                    )
                
                # Process the converted WAV file
                recognizer = sr.Recognizer()
                try:
                    with sr.AudioFile(wav_path) as source:
                        audio_data = recognizer.record(source)
                        extracted_text = recognizer.recognize_google(audio_data)
                except Exception as e:
                    raise Exception(f"Recognition failed. Original audio saved at {mp3_path}. Error: {str(e)}")
                finally:
                    # Clean up temporary WAV file
                    os.unlink(wav_path)
            
            # Convert text to braille
            if extracted_text:
                braille_text = text_to_braille(extracted_text)
                
        except sr.UnknownValueError:
            error_msg = "Could not understand audio"
        except sr.RequestError as e:
            error_msg = f"Could not request results: {e}"
        except Exception as e:
            error_msg = f"Error processing audio: {str(e)}"
            return render(request, 'converter/audio_to_braille.html', {
                'form': form,
                'error': error_msg,
                'extracted_text': extracted_text,
                'braille_text': braille_text
            })
    
    return render(request, 'converter/audio_to_braille.html', {
        'form': form,
        'extracted_text': extracted_text,
        'braille_text': braille_text
    })



def process_recording(audio_data):
    """Process base64 encoded audio recording"""
    try:
        # Remove data URL prefix if present
        if ',' in audio_data:
            audio_data = audio_data.split(',')[1]
        
        # Convert base64 to bytes
        audio_bytes = base64.b64decode(audio_data)
        print(text)
        # Create temp directory if it doesn't exist
        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        mp3_filename = f"recording_{timestamp}.mp3"
        mp3_path = os.path.join(temp_dir, mp3_filename)
        
        # Save as MP3
        with open(mp3_path, 'wb') as mp3_file:
            mp3_file.write(audio_bytes)
        
        # Convert to WAV and process
        sound = AudioSegment.from_file(mp3_path)
        with NamedTemporaryFile(suffix='.wav', delete=False) as tmp_wav:
            wav_path = tmp_wav.name
            sound.set_frame_rate(16000).set_channels(1).export(
                wav_path, 
                format="wav",
                codec="pcm_s16le"
            )
        
        # Recognize speech
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
        
        # Clean up
        os.unlink(wav_path)
        os.unlink(mp3_path)
        
        return text
    
    except Exception as e:
        print(f"Error processing recording: {e}")
        return ""


# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'braille_converter.settings')
django.setup()
def get_llm_response(
    prompt: str,
    model_name: str = "mistralai/Mixtral-8x7B-Instruct-v0.1",  # Free tier available
    max_words: int = 20
) -> Optional[str]:
    """
    For llm part you have to put your hugging face read type api here otherwise it not works
    """

    HUGGINGFACE_API_KEY = "API_KEY_HERE" # Replace with your actual API key


    API_URL = f"https://api-inference.huggingface.co/models/{model_name}"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

    try:
        # Format prompt for instruct models
        prefix = ""#f"You are a chatbot for our software Drishyam, so respond accordingly to this prompt in maximum {max_words} words:"
        suffix = "give answer in max 20 words."
        formatted_prompt = f"{prefix} {prompt} {suffix}".strip()
        response = requests.post(
            API_URL,
            headers=headers,
            json={
                "inputs": formatted_prompt,
                "parameters": {
                    "max_new_tokens": max_words * 3,  # ~3 tokens per word
                    "return_full_text": False  # Don't repeat the prompt
                }
            }
        )
        
        # Handle API errors
        if response.status_code != 200:
            error_msg = response.json().get("error", "Unknown error")
            raise Exception(f"API Error {response.status_code}: {error_msg}")

        return response.json()[0]['generated_text']

    except Exception as e:
        print(f"Error: {str(e)}")
        return None