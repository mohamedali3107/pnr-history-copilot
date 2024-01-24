import os
from PyPDF2 import PdfReader
import pickle
import streamlit as st
import utils

from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file

openai.api_key = os.environ["OPENAI_API_KEY"]
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_BASE"] = "https://ama-openai-uks.openai.azure.com/"
os.environ["OPENAI_API_VERSION"] = "2023-05-15"

deployment_name = "gpt-4-60rpm"
embedding_model = "text-embedding-ada-002-2100rpm"

# Interface

st.title("🛩️💬 AI Rules for Amadeus")


class PDFChatBot:
    def __init__(self) -> None:
        self.qa_chain = None
        self.pdf = None

    @st.spinner("Reading PDF...")
    def load_pdf(self, pdf):
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

    @st.spinner("Splitting PDF...")
    def split_pdf(self, text):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=200,
        )
        chunks = text_splitter.split_text(text)
        return chunks

    @st.spinner("Embedding...")
    def embed_pdf(self, chunks):
        embeddings = OpenAIEmbeddings(deployment=embedding_model, chunk_size=16)
        VectorStore = FAISS.from_texts(chunks, embeddings)
        return VectorStore

    @st.spinner("Analyzing PDF...")
    def get_vector_store(self, pdf):
        store_name = pdf.name[:-4]
        if os.path.exists(f"{store_name}.pkl"):
            st.sidebar.write("PDF already analyzed, loading existing vector store.")
            with open(f"{store_name}.pkl", "rb") as f:
                VectorStore = pickle.load(f)
        else:
            VectorStore = self.embed_pdf(self.split_pdf(self.load_pdf(pdf)))
            with open(f"{store_name}.pkl", "wb") as f:
                pickle.dump(VectorStore, f)
        return VectorStore

    @st.cache_resource
    def init_memory(_self):
        return ConversationBufferMemory(memory_key="chat_history", output_key="answer")

    def setup_qa_chain(self, pdf):
        VectorStore = self.get_vector_store(pdf)

        retriever = VectorStore.as_retriever(
            search_type="similarity", search_kwargs={"k": 5}
        )

        llm = AzureChatOpenAI(deployment_name=deployment_name, streaming=True)

        template = """
INSTRUCTIONS : If the USER QUESTION asks you the keypoints of the
document (or asks you in general what is in the CONTEXT), fill the
TEMPLATE below with the informations taken from the CONTEXT and
respect the displaying format. If the user asks you a specific
question, try to find the answer in the CONTEXT and don't fill the
TEMPLATE. Don't try to make up an answer if you don't know the
answer, just say that you don't know.

CONTEXT: "{context}"

CHAT HISTORY: "{chat_history}"

USER QUESTION: "{question}"

HELPFUL ANSWER:"""

        prompt = PromptTemplate(
            input_variables=["context", "chat_history", "question"], template=template
        )

        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            memory=self.init_memory(),
            get_chat_history=lambda h: h,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": prompt},
            verbose=True,
        )

        return qa_chain

    def get_input_pdf(self):
        st.sidebar.title("PDF Dropzone")

        pdf = st.sidebar.file_uploader("Choose your pdf file", type="pdf")

        if not pdf:
            st.error("Please upload a PDF file to start.")
            st.stop()

        self.pdf = pdf
        print("Creating QA chain...\n")
        self.qa_chain = self.setup_qa_chain(pdf)

    @utils.enable_chat_history
    def main(self):
        user_query = st.chat_input("Ask me anything about your PDF !")

        if user_query:
            prompt = (
                user_query
                + """ \n
TEMPLATE:
Changes condition before departure: EUR [value] \n
Changes condition no show at first flight: EUR [value] \n
Changes condition after departure: EUR [value] \n
Changes condition no show at subsequent flight: EUR [value] \n
Refund condition for cancellation before departure: [Allowed or not] \n
Refund condition no show at first flight: [Allowed or not] \n
Refund condition no show at subsequent flight: [Allowed or not] \n
Minimum stay: Travel must commence on/after [Date], from [City] \n
Maximum stay: Travel must commence before [Date], from [City] \n"""
            )

            utils.display_msg(user_query, "user")

            response = self.qa_chain({"question": prompt})["answer"]

            utils.display_msg(response, "assistant")


if __name__ == "__main__":
    bot = PDFChatBot()
    bot.get_input_pdf()
    bot.main()
