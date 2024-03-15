import requests

API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
headers = {"Authorization": "Bearer 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"}


def query(filename):
    with open(filename, "rb") as file:
        data = file.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()


output = query("ai_audio.flac")

print(output)
