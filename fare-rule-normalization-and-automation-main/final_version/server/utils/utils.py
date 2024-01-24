import fitz
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

deployment_name = "gpt-4-0613"
embedding_model_name = "text-embedding-ada-002"


def extract_text_from_pdf(pdf):
    """
    Extract the text inside a PDF file.

    Parameters:
    - pdf: A file with a pdf extension.

    Returns:
    - text (str): The corresponding text.
    """
    pdf_document = fitz.open(stream=pdf, filetype="pdf")
    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        text += page.get_text("text")
    return text


def split_text(text):
    """
    Split a text (str) using Recursive CharacterTextSplitter() method.

    Parameters:
    - text (str): The text you want to split.

    Returns:
    - chunks (list(str)): The chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=200,
    )
    chunks = text_splitter.split_text(text)
    return chunks


def embed_chunks(chunks):
    """
    Do the embedding of the chunks using OpenAIEmbeddings() and our deployment model.

    Parameters:
    - chunks (list(str)): The chunks you want to embed.

    Returns:
    - VectoreStore (vectorestore): The vectore store corresponding to the chunks.
    """
    embeddings = OpenAIEmbeddings(deployment=embedding_model_name, chunk_size=16)
    VectorStore = FAISS.from_texts(chunks, embeddings)
    return VectorStore


def pdf_to_vector_store(pdf):
    """
    Use extract_text_from_pdf(), split_text() and embed_chunks() methods to return the corresponding vectore store of a pdf.

    Parameters:
    - pdf: The pdf you want to vectorise.

    Returns:
    - VectoreStore (vectorestore): The vectore store corresponding to the pdf file.
    """
    text = extract_text_from_pdf(pdf)
    chunks = split_text(text)
    vector_store = embed_chunks(chunks)
    return vector_store
