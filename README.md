1)clone the repo <br>
2)cd braille_converter <br>
3)./setup.bat<br>
for running = <br>
(in terminal type)<br>
venv\Scripts\activate <br>
python manage.py runserver <br>
<br>
<br>
for closing ctrl + c in same terminal

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////<br>
for chatbot part you have to make your own huggingface read type api key  and put it into views.py in get_llm_response function<br>
<br>

def get_llm_response(<br>
    prompt: str,<br>
    model_name: str = "mistralai/Mixtral-8x7B-Instruct-v0.1",  # Free tier available<br>
    max_words: int = 20<br>
) -> Optional[str]:<br>
    """<br>
    For llm part you have to put your hugging face read type api here otherwise it not works<br>
    """<br>
<br>
    HUGGINGFACE_API_KEY = "API_KEY_HERE" # Replace with your actual API key   <<<<<<<<<<<<<<<<<<<<<<HERE
