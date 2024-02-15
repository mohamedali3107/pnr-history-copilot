import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS

import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file

openai.api_key = os.environ["OPENAI_API_KEY"]
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_BASE"] = "https://ama-openai-uks.openai.azure.com/"
os.environ["OPENAI_API_VERSION"] = "2023-05-15"


def split(text: str, splitter="default"):
    """Return chunks of texts as split by the splitter options.

    Parameters:
    - text (str): the text to split
    - Optional splitter (langchain splitter to apply on a text): the chosen splitter

    Return:
    list: the list of chunks of text
    """
    if splitter == "default":
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1100, chunk_overlap=200, separators=["\n\n", "\n", " ", ""]
        )
    return splitter.split_text(text)


def text_to_vector_store(text: str, embedding_model="default", splitter="default"):
    """Return a vectorstore based on a text.

    Parameters:
    - text (str): the text to be used
    - Optional embedding_model (typically OpenAIEmbeddings instance): the model used to embed the text chunks

    Return:
    VectorStore: the vectorstore containing the embbeded chunks of text
    """
    if embedding_model == "default":
        embedding_model = OpenAIEmbeddings(
            deployment="text-embedding-ada-002", chunk_size=16
        )

    split_text = split(text, splitter)

    vector_store = FAISS.from_texts(split_text, embedding_model)
    return vector_store
