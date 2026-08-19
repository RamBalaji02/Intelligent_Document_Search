import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

print("API KEY LOADED:", bool(api_key))

if not api_key:
    print("ERROR: API key not found in .env")
    exit()

url = "https://api.openai.com/v1/responses"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

payload = {
    "model": "gpt-5-mini",
    "input": "Explain machine learning in one simple sentence."
}

try:
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=60
    )

    print("\nSTATUS CODE:")
    print(response.status_code)

    print("\nRESPONSE:")
    print(response.text)

except Exception as e:
    print("\nERROR:")
    print(e)