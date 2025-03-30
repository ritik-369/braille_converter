from django.shortcuts import render
from .forms import BrailleTextForm, ImageUploadForm
from .utils import text_to_braille, braille_to_text, extract_text_from_image, text_to_speech
from .models import HandwrittenImage
import os
from django.conf import settings

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

            print(f"Extracted text: {extracted_text}")  # Debugging line

            if not extracted_text.strip():
                return render(request, 'converter/image_to_audio.html', 
                              {'form': form, 'error': 'Failed to extract text from image.'})

            audio_file = text_to_speech(extracted_text)

            if not audio_file:
                return render(request, 'converter/image_to_audio.html', 
                              {'form': form, 'error': 'Failed to generate audio.'})

    return render(request, 'converter/image_to_audio.html', {'form': form, 'audio_file': audio_file,'MEDIA_URL': settings.MEDIA_URL})
