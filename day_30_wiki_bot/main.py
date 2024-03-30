import json
import os

import dotenv
import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WikipediaLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAI

dotenv.load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["model"] = os.getenv("MODEL")
os.environ["base_url"] = os.getenv("BASE_URL")

st.title = "Wiki Bot"

with st.sidebar:
    user_input = st.text_input("Wiki Search", "Bill Gates")

    if user_input is not None:
        st.write("Thanks for the input!")

button_enabled = st.sidebar.button("Retrieve Wiki Data and Ask Away!")
question_input = st.text_input("Question:", "Who is Bill Gates?")

if button_enabled and len(question_input) > 0:
    documents = WikipediaLoader(query=user_input, load_max_docs=2, doc_content_chars_max=10000).load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
    docs = text_splitter.split_documents(documents)

    # create a vectorstore
    vectorstore = Chroma(
        collection_name="full_documents",
        embedding_function=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                                 model_kwargs={'device': 'cpu'})
    )
    vectorstore.add_documents(docs)

    qa = ConversationalRetrievalChain.from_llm(
        OpenAI(base_url=os.getenv("BASE_URL"), temperature=0),
        vectorstore.as_retriever(),
        memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    )

    response = qa({"question": question_input})
    current_json = json.dumps(response["answer"])
    cleaner_json_content = current_json.replace("\\", "").replace("\n\n", "")
    final_output = json.dumps(cleaner_json_content)

    if response:
        print(response)
        st.text_area(
            "Answer",
            final_output,
            height=400
        )

        st.write(f'Here is your summary!')
