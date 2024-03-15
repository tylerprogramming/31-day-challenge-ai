import requests
import autogen
from typing import Annotated
import json

API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
headers = {"Authorization": "Bearer your_token"}

llm_config = {
    "config_list": autogen.config_list_from_json(
        env_or_file="OAI_CONFIG_LIST.json",
    ),
    "temperature": 0,
    "seed": 41
}


def query(filename):
    with open(filename, "rb") as file:
        data = file.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()


output = query("ai_audio.flac")

print(output)

# Create an agent workflow and run it
assistant = autogen.AssistantAgent(name="assistant", llm_config=llm_config)
translator = autogen.AssistantAgent(name="translator", llm_config=llm_config,
                                    system_message="I will translate text into the language I am given, then save it to a file.")
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    code_execution_config=False,
    human_input_mode="NEVER",
)


@user_proxy.register_for_execution()
@assistant.register_for_llm(description="Get the audio text then transcribe it")
def transcribe() -> str:
    with open("ai_audio.flac", "rb") as file:
        data = file.read()
    response = requests.post(API_URL, headers=headers, data=data)

    return response.text
    # chat_result = user_translator.initiate_chat(
    #     translator,
    #     message=f"Translate the audio text: {response.text} to the "
    #             f"language {language} and return the newly translated "
    #             f"text.",
    #     max_turns=16)
    # return chat_result.summary


@user_proxy.register_for_execution()
@translator.register_for_llm(description="Get the audio text then translate it")
def translate(translated: Annotated[str, "The language to translate to"]) -> str:
    print("the translate text", translated)
    with open("new_translated.txt", "w") as file:
        file.write(translated)

    return translated


group_chat = autogen.GroupChat(agents=[user_proxy, assistant, translator], messages=[], max_round=10)
manager = autogen.GroupChatManager(groupchat=group_chat, llm_config=llm_config)

# user_proxy.initiate_chats(
#     {
#
#     }
# )

user_proxy.initiate_chat(
    manager,
    message="The assistant will take an audio file and transcribe it, then the translator will take that transcribed "
            "text and translate it to the french language.  That is all that needs done.  No need to write code, just use the correct function calls."
)

# user_proxy.initiate_chat(
#     assistant,
#     message="I need the assistant agent to transcribe an audio file, then have the "
#             "translator agent translate that to the french language.  Translate the text and make sure it gets saved "
#             "to a file.")
