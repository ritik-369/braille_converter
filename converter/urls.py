from django.urls import path
from .views import *

urlpatterns = [
    path('', menu_view, name='home'),  # Homepage redirects to the menu
    path('text-to-braille/', text_to_braille_view, name='text_to_braille'),  # Fix: Use underscores
    path('braille-to-text/', braille_to_text_view, name='braille_to_text'),
    path('image-to-braille/', image_to_braille_view, name='image_to_braille'),
    path('image-to-audio/', image_to_audio_view, name='image_to_audio'),
    path('audio-to-braille/', audio_to_braille_view, name='audio_to_braille'),
    path('chatbot/', chatbot_view, name='chatbot'),
]
