import requests
import api
import agents
from typing import Annotated
from PIL import Image
import io
from random import randint


# inference server query for image 2 text
def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(api.API_URL_IMG, headers=api.headers_img, data=data)
    return response.json()


# inference server query text 2 speech
def query_speech(message):
    response = requests.post(api.API_URL_SPEECH, headers=api.headers, json=message)
    return response.content


def query_create_image(message):
    response = requests.post(api.API_URL, headers=api.headers, json=message)
    return response.content


# the function to take in prompt and convert to image and save to a file
@agents.user_proxy.register_for_execution()
@agents.image_creation.register_for_llm(description="Get the text to convert to image and save to file")
def create_image(message: Annotated[str, "The response from the LLM"]) -> str:
    print(message)

    image_bytes = query_create_image(message)

    file_name = "filename_test.png"

    Image.open(io.BytesIO(image_bytes)).save(file_name)
    return message


@agents.user_proxy.register_for_execution()
@agents.image_describer.register_for_llm(description="Take the image generated, and then describe it")
def image_recognition(image: Annotated[str, "The image to describe"]) -> str:
    print(image)

    output = query("filename_test.png")
    return output


@agents.user_proxy.register_for_execution()
@agents.audio_creator.register_for_llm(description="Get the text to convert to audio and save to file")
def audio_creation(message: Annotated[str, "The response from the LLM"]) -> str:
    audio = query_speech({
        "inputs": message,
    })

    with open('ai_audio.flac', 'wb') as file:
        file.write(audio)

    return message


def shake(t, pos):
    speed = 1
    d = randint(0, 4)
    if 0 == d:
        return pos[0], pos[1] + speed
    if 1 == d:
        return pos[0] - speed, pos[1]
    else:
        return pos[0] + speed, pos[1]
