import autogen

zephyr = {
    "config_list": [
        {
            "model": "TheBloke/stablelm-zephyr-3b-GGUF/stablelm-zephyr-3b.Q4_K_S.gguf",
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
