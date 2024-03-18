from typing import Annotated
import autogen
import random

config_list = autogen.config_list_from_json(
    env_or_file="OAI_CONFIG_LIST.json",
    filter_dict={
        "model": ["gpt-3.5-turbo"]
    },
)

llm_config = {
    "config_list": config_list,
    "timeout": 120,
}

assistant1 = autogen.AssistantAgent(
    name="assistant1",
    system_message="You are to save to a file.",
    llm_config=llm_config,
)

assistant2 = autogen.AssistantAgent(
    name="assistant2",
    system_message="You are to save to a file.",
    llm_config=llm_config,
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config=False
)


@user_proxy.register_for_execution()
@assistant1.register_for_llm(description="Save to file")
@assistant2.register_for_llm(description="Save to file")
def save_to_file(message: Annotated[str, "The response from the model"]) -> str:
    print(message)

    random_number = random.randint(1, 1000)

    with open("saved_file_" + str(random_number) + ".txt", 'w') as file:
        file.write(message)

    return message


group_chat = autogen.GroupChat(agents=[user_proxy, assistant1, assistant2], messages=[], max_round=12)
manager = autogen.GroupChatManager(groupchat=group_chat, llm_config=llm_config)

# # start the conversation
# user_proxy.initiate_chat(
#     manager,
#     message="Have assistant1 agent give a quote from a famous author, and then when thats done, have assistant2 give "
#             "another quote from a famous author.",
# )

user_proxy.initiate_chats(
    [
        {
            "recipient": assistant1,
            "message": "give a quote from a famous author",
            "clear_history": True,
            "silent": False,
            "summary_method": "last_msg",
        },
        {
            "recipient": assistant2,
            "message": "give me a quote from a different famous author, make sure it isn't the same quote from last "
                       "llm call",
            "summary_method": "reflection_with_llm",
        }
    ]
)
