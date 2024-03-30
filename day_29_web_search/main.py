import autogen

from autogen.agentchat.contrib.web_surfer import WebSurferAgent

llm_config = {
    "timeout": 600,
    "cache_seed": 42,
    "config_list": autogen.config_list_from_json(
        "OAI_CONFIG_LIST.json"),
    "temperature": 0,
}

summarizer_llm_config = {
    "timeout": 600,
    "cache_seed": None,
    "config_list": autogen.config_list_from_json(
        "OAI_CONFIG_LIST.json"),
    "temperature": 0,
}

web_surfer = WebSurferAgent(
    "web_surfer",
    llm_config=llm_config,
    summarizer_llm_config=summarizer_llm_config,
    browser_config={"viewport_size": 4096, "bing_api_key": "1111"},
)

user_proxy = autogen.UserProxyAgent(
    "user_proxy",
    human_input_mode="NEVER",
    code_execution_config=False,
    default_auto_reply="",
    is_termination_msg=lambda x: True,
)

# task1 = """
# Search the web for information about Microsoft AutoGen
# """
# user_proxy.initiate_chat(web_surfer, message=task1)
# task2 = "Summarize these results"
# user_proxy.initiate_chat(web_surfer, message=task2, clear_history=False)
# task3 = "Click the 'Getting Started' result"
# user_proxy.initiate_chat(web_surfer, message=task3, clear_history=False)


task4 = """Find Microsoft's Wikipedia page."""
user_proxy.initiate_chat(web_surfer, message=task4, clear_history=False)
task5 = """Scroll down."""
user_proxy.initiate_chat(web_surfer, message=task5, clear_history=False)
task6 = """Where is there total revenue?"""
user_proxy.initiate_chat(web_surfer, message=task6, clear_history=False)
