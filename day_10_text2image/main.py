import requests
import random
import io
import autogen
from PIL import Image
from typing import Annotated

# api and headers
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": "Bearer your_token"}

# the llm_config
llm_config = {
    "config_list": autogen.config_list_from_json(
        env_or_file="OAI_CONFIG_LIST.json",
    ),
    "temperature": 0.5,
    "seed": 41
}

# Create the agent workflow
assistant = autogen.AssistantAgent(name="assistant", llm_config=llm_config)
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    code_execution_config=False,
    human_input_mode="NEVER"
)


# the function to take in prompt and convert to image and save to a file
@user_proxy.register_for_execution()
@assistant.register_for_llm(description="Get the text to convert to image and save to file")
def create_image(message: Annotated[str, "The response from the LLM"]) -> str:
    print(message)

    response = requests.post(API_URL, headers=headers, json=message)
    image_bytes = response.content

    random_number = random.randint(1, 1000000)
    file_name = "filename_" + str(random_number) + ".png"

    Image.open(io.BytesIO(image_bytes)).save(file_name)
    return message


user_proxy.initiate_chat(
    assistant, message="Create a prompt for image generation ai with mario.  Be creative.  The style "
                       "should be dreamy."
)
