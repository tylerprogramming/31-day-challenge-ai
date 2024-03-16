import autogen

llm_config = {
    "config_list": autogen.config_list_from_json(
        env_or_file="OAI_CONFIG_LIST.json",
    ),
    "temperature": 0,
    "seed": 42
}

# Create the agent workflow
image_creation = autogen.AssistantAgent(
    name="image_creation",
    system_message="You will be the first agent to perform a task, and that will be to create an image.",
    llm_config=llm_config)

image_describer = autogen.AssistantAgent(
    name="image_describer",
    system_message="""
        Your job is to describe an image.  The Assistant Agent will create a new file image based on a prompt, and
        then you will look at that image and describe in vivid detail what it's about.
    """,
    llm_config=llm_config
)

audio_creator = autogen.AssistantAgent(
    name="audio_creator",
    system_message="""
        You job is to create speech from text.  The image_describer will give you text which is describing an image,
        then you will create audio from that.
    """,
    llm_config=llm_config
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    code_execution_config=False,
    human_input_mode="NEVER"
)

group_chat = autogen.GroupChat(agents=[user_proxy, image_creation, image_describer, audio_creator], messages=[], max_round=10)
manager = autogen.GroupChatManager(groupchat=group_chat, max_consecutive_auto_reply=10, llm_config=llm_config)
