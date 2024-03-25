import os
from typing import Annotated

import autogen
import markdown
import functions

from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)
from langchain_openai import ChatOpenAI


os.environ["OPENAI_API_KEY"] = "sk-1111"
os.environ["model"] = "gpt-3.5-turbo"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

credentials = get_gmail_credentials(
    token_file="token.json",
    scopes=["https://mail.google.com/"],
    client_secrets_file="credentials.json",
)
api_resource = build_resource_service(credentials=credentials)
toolkit = GmailToolkit(api_resource=api_resource)

text = functions.get_transcription_from_yt_video("https://www.youtube.com/watch?v=1bUy-1hGZpI")

config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST.json")
llm_config = {"config_list": config_list}

writer = autogen.AssistantAgent(
    name="Writer",
    llm_config={"config_list": config_list},
    system_message="""
    You are a professional writer, known for your insightful and engaging articles.
    You transform complex concepts into compelling narratives.
    You should improve the quality of the content based on the feedback from the user.
    """,
)

user_proxy = autogen.UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    code_execution_config={
        "last_n_messages": 1,
        "work_dir": "tasks",
        "use_docker": False,
    },
)


@user_proxy.register_for_execution()
@writer.register_for_llm(description="Email a blog")
def email_blog(content: Annotated[str, "The blog to email"]) -> str:
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    html = markdown.markdown(content)

    instructions = """You are an assistant."""
    base_prompt = hub.pull("langchain-ai/openai-functions-template")
    prompt = base_prompt.partial(instructions=instructions)

    agent = create_openai_functions_agent(llm, toolkit.get_tools(), prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=toolkit.get_tools(),
        verbose=False,
    )

    agent_executor.invoke(
        {
            "input": f"Can you send an email to tylerreedytlearning@gmail.com with the post created above: {html}, and "
                     f"it should end with Sincerely, Tyler.  We don't need to CC anybody."
        }
    )
    return content


user_proxy.initiate_chat(
    recipient=writer,
    message=f"Create a blog post with the following youtube script with the title, an outline of the main points, "
            f"and then paragraphs explaining and summarizing the script.  Make sure this is formatted with Markdown."
            f": {text}",
    max_turns=2,
    summary_method="last_msg"
)





