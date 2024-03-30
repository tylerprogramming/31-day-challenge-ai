import autogen
from autogen import AssistantAgent, UserProxyAgent

from day_29_custom_model_agents.CustomModelClient import CustomModelClient

config_list_custom = autogen.config_list_from_json(
    "OAI_CONFIG_LIST.json",
    filter_dict={"model_client_cls": ["CustomModelClient"]},
)

assistant = AssistantAgent("assistant", llm_config={"config_list": config_list_custom})
user_proxy = UserProxyAgent(
    "user_proxy",
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
    },
)

assistant.register_model_client(model_client_cls=CustomModelClient)
user_proxy.initiate_chat(assistant, message="Write python code to print Hello World!")

