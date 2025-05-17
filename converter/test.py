import requests
from django.conf import settings
import os
import django

import sys

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'braille_converter.settings')
django.setup()

from django.conf import settings

def get_llm_response(prompt):
    
    try:
        # Using Hugging Face Inference API as an example
        API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
        headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"}
        
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        response.raise_for_status()
        
        # Different LLM APIs return different formats, adjust accordingly
        if isinstance(response.json(), list):
            return response.json()[0]['generated_text']
        else:
            return response.json().get('generated_text', 'No response generated')
    except Exception as e:
        return f"Error getting LLM response: {str(e)}"
    
print(get_llm_response("tell about tony stark"))