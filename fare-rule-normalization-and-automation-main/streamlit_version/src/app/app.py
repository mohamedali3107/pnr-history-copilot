import os
from PyPDF2 import PdfReader
import pickle
import streamlit as st
import utils
import get_fare_rules_from_API as gf
import get_fare_rules_from_DB as gfdb
import scrapping as sc
import prompt_fill_template

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

deployment_name = "gpt-4-0613"
embedding_model_name = "text-embedding-ada-002"


# Interface
st.title(
    """🛩️💬 AI Rules for Amadeus
         """
)


class PDFChatBot:
    def __init__(self) -> None:
        self.qa_chain = None
        self.pdf = None
        self.webtext = None
        self.flight_number = None
        self.date = None
        self.beginning = True
        self.origin_code = None
        self.destination_code = None
        self.iata_code = None

    @st.spinner("Reading PDF...")
    def load_pdf(self, pdf):
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

    @st.spinner("Splitting PDF...")
    def split_text(self, text):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=200,
        )
        chunks = text_splitter.split_text(text)
        return chunks

    @st.spinner("Embedding...")
    def embed_chunks(self, chunks):
        embeddings = OpenAIEmbeddings(
            deployment=embedding_model_name, chunk_size=16)
        VectorStore = FAISS.from_texts(chunks, embeddings)
        return VectorStore

    @st.spinner("Analyzing PDF...")
    def get_vector_store(self, pdf):
        store_name = pdf.name[:-4]
        if os.path.exists(f"{store_name}.pkl"):
            st.sidebar.write(
                "PDF already analyzed, loading existing vector store.")
            with open(f"{store_name}.pkl", "rb") as f:
                VectorStore = pickle.load(f)
        else:
            VectorStore = self.embed_chunks(
                self.split_text(self.load_pdf(pdf)))
            with open(f"{store_name}.pkl", "wb") as f:
                pickle.dump(VectorStore, f)
        return VectorStore

    @st.cache_resource
    def init_memory(_self):
        return ConversationBufferMemory(memory_key="chat_history", output_key="answer")

    def _prompt_qa(self, source=""):
        from_source = "from the " + source if source != "" else ""
        prompt_str = (
            """
            INSTRUCTIONS : Answer the question below accurately based on the provided context
            """
            + from_source
            + """ in between triple backsticks.
            If the question is about a pdf or a website or portal and the context is not from a PDF
            or website or portal, just output 'Unknown', whatever the question.
            If you don't know the answer from the context, output 'Unknown',
            do not make a sentence.
            Do not try to make up answers.

            """
            + source
            + """ CONTEXT: ```{context}```

            CHAT HISTORY: {chat_history}

            USER QUESTION: {question}

            HELPFUL ANSWER: """
        )

        return PromptTemplate(
            input_variables=["context", "chat_history", "question"], template=prompt_str
        )

    def _setup_qa_chain(self, vector_store, prompt_suffix, memory=None):
        print(f"Creating vector store for {prompt_suffix.lower()}...")
        retriever = vector_store.as_retriever(
            search_type="similarity", search_kwargs={"k": 6})

        llm = AzureChatOpenAI(deployment_name=deployment_name,
                              streaming=True, temperature=0)

        if memory is None:
            memory = self.init_memory()

        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            memory=memory,
            get_chat_history=lambda h: h,
            return_source_documents=True,
            combine_docs_chain_kwargs={
                "prompt": self._prompt_qa(prompt_suffix)},
            verbose=True,
        )

        setattr(self, f"qa_chain_{prompt_suffix.lower()}", qa_chain)

        return qa_chain

    def setup_qa_chain_PDF(self, memory=st.session_state.get("memory")):
        return self._setup_qa_chain(
            self.get_vector_store(st.session_state["pdf"]), "PDF", memory
        )

    def setup_qa_chain_Webtext(self, memory=st.session_state.get("memory")):
        return self._setup_qa_chain(
            self.embed_chunks(self.split_text(
                st.session_state["webtext"])), "Webtext", memory
        )

    def setup_qa_chain_ATPCO(self, VectorStoreATPCO, memory=st.session_state.get("memory")):
        return self._setup_qa_chain(VectorStoreATPCO, "ATPCO DATABASE", memory)

    def process_and_display_flight_fares(self, fare_rules_list):
        llm = AzureChatOpenAI(
            deployment_name=deployment_name, streaming=True, temperature=0
        )
        information = []
        i = 1
        for flight in fare_rules_list:
            if "fare_rules" in flight.keys():
                dep, arr, carrier_code, cat, fare_basis, fare_rules = (
                    flight["departure"],
                    flight["arrival"],
                    flight["carrierCode"],
                    flight["category"],
                    flight["fare_basis"],
                    flight["fare_rules"],
                )
                have_fare_rule = True
            else:
                dep, arr, carrier_code, cat, fare_basis, fare_rules = (
                    flight["departure"],
                    flight["arrival"],
                    flight["carrierCode"],
                    flight["category"],
                    "not in ATPCO",
                    [],
                )
                have_fare_rule = False
            header = f"""FLIGHT NUMBER {i} -
            DEPARTURE: {dep} -
            ARRIVAL: {arr} - IATA CODE: {carrier_code} - CATEGORY: {cat} -
            FARE BASIS: {fare_basis}"""

            information.append([header, fare_rules])
            i += 1

        webtext = sc.scrap_text_from_iata(carrier_code)
        self.webtext = webtext
        st.session_state["webtext"] = webtext

        chunks = []
        for info in information:
            if info[1]:
                chunks.append(
                    RecursiveCharacterTextSplitter(
                        chunk_size=1000,
                        chunk_overlap=200,
                    ).split_text(info[1])
                )
            else:
                chunks.append(
                    RecursiveCharacterTextSplitter(
                        chunk_size=1000,
                        chunk_overlap=200,
                    ).split_text("No fare rule")
                )

        embedding_model = OpenAIEmbeddings(
            deployment=embedding_model_name, chunk_size=16
        )

        prompt = prompt_fill_template.prompt
        question = prompt_fill_template.question

        fares_to_display = []

        for i in range(len(chunks)):
            VectorStore = FAISS.from_texts(chunks[i], embedding_model)

            retriever = VectorStore.as_retriever(
                search_type="similarity", search_kwargs={"k": 9}
            )

            qa_chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=retriever,
                combine_docs_chain_kwargs={"prompt": prompt},
                verbose=True,
            )

            answer = qa_chain({"question": question, "chat_history": []})[
                "answer"]

            fare_to_display = information[i][0] + "\n\n" + answer
            fares_to_display.append(fare_to_display)

        chunks_all = []
        for chunk in chunks:
            chunks_all += chunk

        VectorStoreAll = FAISS.from_texts(chunks_all, embedding_model)

        return VectorStoreAll, fares_to_display, have_fare_rule

    @st.spinner("Getting flight information...")
    def give_flight_main_information(self):
        if self.flight_code is None:
            fare_rules_list = gf.get_fare_rules_from_API(
                self.origin_code, self.destination_code, self.iata_code, self.date
            )
        else:
            self.flight_code = int(self.flight_code)
            fare_rules_list = gfdb.get_fare_rules_from_DB(self.flight_code)

        (
            VectorStoreATPCO,
            fares_to_display,
            have_fare_rule,
        ) = self.process_and_display_flight_fares(fare_rules_list)

        return VectorStoreATPCO, fares_to_display, have_fare_rule

    def get_user_input(self):
        st.sidebar.title("Flight Information 🛫")

        origin_code = st.sidebar.text_input(
            label="Origin Code", placeholder="e.g. PAR", key="originCode"
        )
        destination_code = st.sidebar.text_input(
            label="Destination Code", placeholder="e.g. DPS", key="destinationCode"
        )

        iata_code = st.sidebar.text_input(
            label="Airline Code", placeholder="e.g. QR", key="iataCode"
        )

        date = st.sidebar.date_input(
            label="Flight date", key="flight_date", format="YYYY-MM-DD"
        )

        st.sidebar.title("Booking Reference 🛫")

        flight_code = st.sidebar.selectbox(
            label="Booking Reference",
            index=None,
            options=["56568670", "92098075"],
            placeholder="Select a booking reference",
        )

        st.sidebar.title("PDF Dropzone 📄")

        pdf = st.sidebar.file_uploader("Choose your pdf file", type="pdf")

        if not (
            flight_code or (
                origin_code and destination_code and iata_code and date)
        ):
            st.sidebar.error("Please fill flight information to start.")
            st.stop()

        self.pdf = pdf
        st.session_state["pdf"] = pdf

        self.pdf_paragraph(pdf)

        self.origin_code = origin_code
        self.destination_code = destination_code
        self.iata_code = iata_code
        self.date = date
        self.flight_code = flight_code

    def start_discussion(self):
        if not st.session_state.get("started"):
            (
                VectorStoreATPCO,
                fares_to_display,
                have_fare_rule,
            ) = self.give_flight_main_information()
            st.session_state["memory"] = self.init_memory()
            qa_chain_ATPCO = self.setup_qa_chain_ATPCO(VectorStoreATPCO)
            st.session_state["started"] = True
            return fares_to_display, qa_chain_ATPCO, have_fare_rule
        return None

    @st.spinner("Retrieving information from the trade portal...")
    def web_paragraph(self):
        # Add small paragraph if there is a website associated
        if st.session_state["webtext"] is not None:
            if "chainWebtext" not in st.session_state:
                st.session_state["chainWebtext"] = self.setup_qa_chain_Webtext(
                )
            qa_chain_Webtext = st.session_state["chainWebtext"]
            question_portal_paragraph = """You are assisting a travel agent with providing
                a customer with practical and useful information about its reservation conditions:
                change, refund, special situations...

                Your task is to identify and list some key conditions from the website content
                provided to you as a context, and output them into at most 5 clear and
                concise bullet points.

                Pay special attention to exceptional conditions linked to specific events,
                such as covid, sanitary situations, natural disasters.
                """
            mini_paragraph_web = qa_chain_Webtext(
                {"question": question_portal_paragraph})["answer"]
            utils.display_msg(
                f"Key points retrieved from the airline trade portal :\n{mini_paragraph_web}", "assistant")

    @st.spinner("Retrieving information from the PDF...")
    def pdf_paragraph(self, pdf):
        # Add small paragraph about the pdf
        if pdf != st.session_state.get("previous_pdf"):
            print("New PDF uploaded!")
            st.session_state.previous_pdf = pdf

            if "chainPDF" not in st.session_state:
                st.session_state["chainPDF"] = self.setup_qa_chain_PDF()
            qa_chain_PDF = st.session_state["chainPDF"]
            mini_paragraph_pdf = qa_chain_PDF(
                {"question": "You are a travel agent assistant, give me 3 useful information included in this PDF in bullet points."})["answer"]
            utils.display_msg(
                f"Key points retrieved from the PDF :\n{mini_paragraph_pdf}", "assistant")

    @utils.enable_chat_history
    def run_chat(self):
        discussion_start = self.start_discussion()
        if discussion_start:
            fares_to_display, qa_chain_ATPCO, have_fare_rule = discussion_start
            for fare in fares_to_display:
                if have_fare_rule:
                    utils.display_msg(fare, "assistant")
                else:
                    utils.display_msg(fare.split('\n\n')[0], "assistant")
            self.web_paragraph()
            st.session_state["chain"] = qa_chain_ATPCO

            if have_fare_rule:
                utils.display_msg(
                    """You can now ask me anything about the flight and your
                    pdf! I also have complementary info thanks to
                    the company website""",
                    "assistant",
                )
            else:
                utils.display_msg(
                    """There was no fare note in the ATPCO database. You can now ask me anything
                    about your pdf! I also have complementary info thanks to
                    the company website""",
                    "assistant",
                )

        qa_chain_ATPCO = st.session_state["chain"]
        user_query = st.chat_input("""Write here your questions...""")

        if user_query:
            utils.display_msg(user_query, "user")
            response = qa_chain_ATPCO({"question": user_query})["answer"]

            if response == "Unknown" and st.session_state["pdf"] is not None:
                if "chainPDF" not in st.session_state:
                    st.session_state["chainPDF"] = self.setup_qa_chain_PDF()
                qa_chain_PDF = st.session_state["chainPDF"]

                response = qa_chain_PDF({"question": user_query})["answer"]

            if response == "Unknown" and st.session_state["webtext"] is not None:
                if "chainWebtext" not in st.session_state:
                    st.session_state["chainWebtext"] = self.setup_qa_chain_Webtext(
                    )
                qa_chain_Webtext = st.session_state["chainWebtext"]

                response = qa_chain_Webtext({"question": user_query})["answer"]

            if response == "Unknown":
                response = """I was not able to find the answer to your query, please
                            reformulate and/or upload a pdf file that may contain the
                            piece of information you are looking for."""

            utils.display_msg(response, "assistant")


if __name__ == "__main__":
    bot = PDFChatBot()
    bot.get_user_input()
    bot.run_chat()
