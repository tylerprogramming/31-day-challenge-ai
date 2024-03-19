import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI

os.environ["OPENAI_API_KEY"] = "sk-1111"
os.environ["model"] = "gpt-3.5-turbo"
os.environ["base_url"] = "http://localhost:1234/v1"

folder_path = "faiss_vector_db"

if __name__ == "__main__":
    print("starting")

    embeddings = OpenAIEmbeddings()

    if not os.path.exists(folder_path):
        pdf_path = "/day_19_read_pdf/ancient_rome.pdf"
        loader = PyMuPDFLoader(file_path=pdf_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=30)
        docs = text_splitter.split_documents(documents)

        # stored in ram in local machine
        vectorstore = FAISS.from_documents(documents=docs, embedding=embeddings)
        vectorstore.save_local(folder_path)

    my_vectorstore = FAISS.load_local(folder_path, embeddings, allow_dangerous_deserialization=True)
    qa = RetrievalQA.from_chain_type(llm=OpenAI(), retriever=my_vectorstore.as_retriever(), chain_type="map_reduce")
    response = qa.invoke("Give me a vocabulary definition directly word for word from this pdf from chapter 10")
    print(response)
    print("done")








