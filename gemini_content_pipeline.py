import os
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
print("Checking your available models...")
for m in client.models.list():
    if 'generateContent' in m.supported_methods:
        print(f" - {m.name}")