import os
import autogen
import dotenv
import functions

dotenv.load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["model"] = os.getenv("model")
os.environ["base_url"] = os.getenv("base_url")

text = functions.get_transcription_from_yt_video("https://www.youtube.com/watch?v=T-D1OfcDW1M")

config_list = autogen.config_list_from_dotenv(dotenv_file_path=".")
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
    code_execution_config=False
)

user_proxy.initiate_chat(
    recipient=writer,
    message=f"Create a blog post with the following youtube script with the title, an outline of the main points, "
            f"and then paragraphs explaining and summarizing the script.  Make sure this is formatted with Markdown."
            f": {text}",
    max_turns=2,
    summary_method="last_msg"
)
