from django.urls import path
from .views import menu_view, text_to_braille_view, braille_to_text_view, image_to_braille_view, image_to_audio_view

urlpatterns = [
    path('', menu_view, name='menu'),  # Homepage redirects to the menu
    path('text-to-braille/', text_to_braille_view, name='text_to_braille'),  # Fix: Use underscores
    path('braille-to-text/', braille_to_text_view, name='braille_to_text'),
    path('image-to-braille/', image_to_braille_view, name='image_to_braille'),
    path('image-to-audio/', image_to_audio_view, name='image_to_audio'),
]
