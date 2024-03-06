import os

from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import GitLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

os.environ["OPENAI_API_KEY"] = "sk-1111"

index_name = "faiss_autogen"

question = """How does AutoGen use multimodal agents?."""
# question = """Can you please give a detailed summary of what AutoGen is?"""
# question = """
# Write python code for 3 agents, 2 assistant agents and another being a user agent, the assistant agents
# will be a writer, and critic.  The user agent will just be simple. We also need to create a group chat and initiate
# it.  Create a config_list based on examples from other Autogen code examples. Have all the correct imports,
# the correct code for each agent, and initiate the group chat asking a message about the top 5 longest rivers in the
# world. Look at example code from AutoGen in order to understand how to do this if needed.  I don't want a simplified
# version, give me the full version.  Only return code, nothing else.  The agents should be AutoGen agents, not openai.
# Make sure to use the UserAgent and AssistantAgent, GroupChat and GroupChatManager agents to create the group chat and
# initiate the chat with.
# """


def ingest_docs(question) -> str:
    if not os.path.exists(index_name):
        loader = GitLoader(repo_path="docs/autogen")
        raw_documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=20,
            separators=["\n\n", "\n", " ", ""]
        )
        documents = text_splitter.split_documents(documents=raw_documents)
        print(f"Split into {len(documents)} chunks")

        embeddings = OpenAIEmbeddings()

        # stored in ram in local machine
        vectorstore = FAISS.from_documents(documents=documents, embedding=embeddings)
        vectorstore.save_local(index_name)

    embeddings = OpenAIEmbeddings()
    my_vectorstore = FAISS.load_local(index_name, embeddings)
    qa = RetrievalQA.from_chain_type(llm=ChatOpenAI(model="gpt-4"), retriever=my_vectorstore.as_retriever(),
                                     chain_type="stuff")
    response = qa.invoke({"query": question})
    print("done")

    return response["result"]


if __name__ == "__main__":
    response = ingest_docs(question)
    print(response)
