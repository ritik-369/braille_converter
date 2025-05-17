prompt = "xyz"
max_words = 10
prefix = f"You are a chatbot for our software Drishyam, so respond accordingly to this prompt in maximum {max_words} words:"
suffix = ""
formatted_prompt = f"{prefix} {prompt} {suffix}".strip()
print(formatted_prompt)
