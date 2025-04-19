# from langchain.document_loaders import DirectoryLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
# from langchain.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import openai 
from dotenv import load_dotenv
import os
import shutil
from langchain_qdrant import QdrantVectorStore

from splitter.split_data import split_text, splitter_main

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

DATA_PATH = "data/books"

def main():
    generate_data_store()

def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    documents = loader.load()
    return documents

def generate_data_store():
    documents = load_documents()
    chunks = splitter_main(documents)
    return chunks

def save_embeddings():
    embedder = OpenAIEmbeddings(
        model="text-embedding-3-large",
        api_key=openai.api_key
    )
    vector_store = QdrantVectorStore.from_documents(
        documents = generate_data_store(),
        url="http://localhost:6333",
        collection_name="book1",
        embedding=embedder
    )

    print("Documents added to vector store.")

if __name__ == "__main__":
    save_embeddings()
