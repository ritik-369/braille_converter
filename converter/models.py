from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class BrailleText(models.Model):
    text = models.TextField()
    braille = models.TextField()

class HandwrittenImage(models.Model):
    image = models.ImageField(upload_to='uploads/')
    extracted_text = models.TextField(blank=True, null=True)


class AudioFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to='audio_files/')
    original_filename = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    braille_text = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Audio file {self.id} - {self.original_filename}"
    

class ChatBotQuery(models.Model):
    INPUT_TYPES = (
        ('text', 'Text'),
        ('audio_file', 'Audio File'),
        ('recording', 'Live Recording'),
    )
    
    OUTPUT_TYPES = (
        ('text', 'Text'),
        ('audio', 'Audio'),
        ('braille', 'Braille'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    input_type = models.CharField(max_length=20, choices=INPUT_TYPES)
    output_type = models.CharField(max_length=20, choices=OUTPUT_TYPES)
    text_input = models.TextField(blank=True, null=True)
    audio_input = models.FileField(upload_to='chatbot_audio_inputs/', blank=True, null=True)
    recording_input = models.TextField(blank=True, null=True)  # For base64 encoded audio
    llm_response = models.TextField(blank=True, null=True)
    audio_response = models.FileField(upload_to='chatbot_audio_responses/', blank=True, null=True)
    braille_response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"ChatBot Query by {self.user.username} at {self.created_at}"