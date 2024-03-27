import anthropic
import autogen
import os

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

message = client.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=4096,
    temperature=0.0,
    system="Respond as if you were a professional engineer.",
    messages=[
        {"role": "user", "content": "Create a simple game of snake for me in python"}
    ]
)

print(message.content[0].text)

zephyr = {
    "config_list": [
        {
            "model": "claude-3-sonnet-20240229",
            "base_url": "http://localhost:1234/v1",
            "api_key": "lm-studio",
        },
    ],
    "cache_seed": None,
}

phi2 = {
    "config_list": [
        {
            "model": "TheBloke/phi-2-GGUF/phi-2.Q6_K.gguf",
            "base_url": "http://localhost:1234/v1",
            "api_key": "lm-studio",
        },
    ],
    "cache_seed": None,
}

phil = autogen.ConversableAgent(
    "Phil (Phi-2)",
    llm_config=phi2,
    system_message="Your name is Phil and you are a comedian in a two-person comedy show.",
)
zep = autogen.ConversableAgent(
    "Zep (Zephyr)",
    llm_config=zephyr,
    system_message="Your name is Zep and you are a comedian in two-person comedy show.",
)

chat_result = phil.initiate_chat(zep, message="Zep, tell me a joke.", max_turns=2)