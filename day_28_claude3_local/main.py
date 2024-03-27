import os
from autogen import AssistantAgent, UserProxyAgent

os.environ[
    "ANTHROPIC_API_KEY"] = "sk-ant-api03-1111-1111"

claude = {
    "config_list": [
        {
            "model": "claude-3-sonnet-20240229",
            "base_url": "http://0.0.0.0:4000",
            "api_type": "open_ai",
            "api_key": "anything",
        },
    ],
    "cache_seed": "44",
    "max_tokens": 4096
}

assistant = AssistantAgent("assistant", llm_config=claude)
user_proxy = UserProxyAgent(
    "user_proxy",
    human_input_mode="NEVER",
    default_auto_reply="...",
    max_consecutive_auto_reply=1,
    code_execution_config=False
)

chat_result = user_proxy.initiate_chat(
    assistant,
    message="Write a full implementation of snake game in python.", max_turns=4)
