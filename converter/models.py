from django.db import models

class BrailleText(models.Model):
    text = models.TextField()
    braille = models.TextField()

class HandwrittenImage(models.Model):
    image = models.ImageField(upload_to='uploads/')
    extracted_text = models.TextField(blank=True, null=True)
