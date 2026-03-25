# lister.py
from google import genai

client = genai.Client(api_key="AIzaSyBSxMbwN6rE0WKr8cPxIAoSZTwIfzFn9w4")

for m in client.models.list():
    print(f"Modelo disponible: {m.name}")




