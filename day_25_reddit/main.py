from langchain_community.document_loaders.reddit import RedditPostsLoader
import autogen

# https://www.reddit.com/prefs/apps/
loader = RedditPostsLoader(
    client_id="id",
    client_secret="secret",
    user_agent="extractor by u/tyler_programming",
    categories=["new"],  # Note: Categories can be only of following value - "controversial" "hot" "new" "rising" "top"
    mode="subreddit",
    search_queries=[
        "openai"
    ],  # List of subreddits to load posts from
    number_posts=3,  # Default value is 10
)

documents = loader.load()

config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST.json")
llm_config = {"config_list": config_list, "seed": 45}

writer = autogen.AssistantAgent(
    name="Writer",
    llm_config={"config_list": config_list},
    system_message="""
    You won't change the information given, just parse the page_content from the reddit post.  No code will
    be written.
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
    message=f"""I need you to extract the page_content and url from each of {documents}, 
            with each document extracted separate from each other.  Make sure this is formatted with Markdown.  Get it ready 
            for an email, but don't add or change what is in the documents.  Make sure to use the FULL page_content
            from the document.

            Create a newsletter from this information with:

            [Newsletter Title Here] - make sure to create a catchy title

            The format for markdown should be:

            Title of the document
            The Page Content
            The Author
            The url
            """,
    max_turns=2,
    summary_method="last_msg"
)
