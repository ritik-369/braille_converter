from django import forms
from .models import HandwrittenImage

class BrailleTextForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, required=True)

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = HandwrittenImage
        fields = ['image']
