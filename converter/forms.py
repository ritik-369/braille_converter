from django import forms
from .models import HandwrittenImage
from .models import AudioFile
from .models import ChatBotQuery

class BrailleTextForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, required=True)

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = HandwrittenImage
        fields = ['image']


class AudioUploadForm(forms.ModelForm):
    class Meta:
        model = AudioFile
        fields = ['audio_file']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['audio_file'].widget.attrs.update({
            'class': 'form-control',
            'accept': 'audio/*'
        })


class ChatBotQueryForm(forms.ModelForm):
    class Meta:
        model = ChatBotQuery
        fields = ['input_type', 'output_type', 'text_input', 'audio_input']
        widgets = {
            'text_input': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'audio_input': forms.FileInput(attrs={'class': 'form-control'}),
            'input_type': forms.Select(attrs={'class': 'form-control', 'id': 'input-type-select'}),
            'output_type': forms.Select(attrs={'class': 'form-control'}),
        }
