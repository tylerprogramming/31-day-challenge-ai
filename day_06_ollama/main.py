import autogen

config_list = autogen.config_list_from_json(
    env_or_file="OAI_CONFIG_LIST.json"
)

assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={"config_list": config_list}
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False
    }
)

user_proxy.initiate_chat(
    assistant,
    message="Write to a python file the code to plot a chart of the top 10 countries by land mass.")