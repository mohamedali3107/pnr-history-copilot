import os
import functions.scraping as sc
import functions.prompt_fill_template as prompt_fill_template
from functions.text_to_vector_store import text_to_vector_store, split
from functions.create_qa_chain import chain_paragraph
from functions.answer_chat import answer_retrieval_chain

from langchain.chat_models import AzureChatOpenAI
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
embedding_model = OpenAIEmbeddings(deployment=embedding_model_name, chunk_size=16)
llm = AzureChatOpenAI(deployment_name=deployment_name, streaming=True, temperature=0)


def get_fare_rules(flight):
    """Return the fare rules of a flight retrieved with an API

    Parameters:
    - flight (dict): a dictionary containing the information of a flight

    Return:
    str: the fare rules (empty string if there were none)
    """
    fare_rules = ""
    if "fare_rules" in flight.keys():
        fare_rules = flight["fare_rules"]
    return fare_rules


def format_flight_info(flights_list):
    """Return the flight information as a list of tuples, plus the carrier code
    (of last flight) and a boolean stating the presence of fare rules (in last flight).

    Parameters:
    flights_list (list): a list of dictionaries with flight information

    Return:
    tuple: the list of reformatted flight information, carrier code and a boolean
    """
    information_flights = []
    i = 1
    for flight in flights_list:
        dep, arr, carrier_code, cat, fare_basis = (
            flight["departure"],
            flight["arrival"],
            flight["carrierCode"],
            flight["category"],
            flight["fare_basis"],
        )
        fare_rules = get_fare_rules(flight)

        header = f"""FLIGHT NUMBER {i} - DEPARTURE: {dep} - ARRIVAL: {arr} - AIRLINE: {carrier_code} - CATEGORY: {cat} - FARE BASIS: {fare_basis}"""

        information_flights.append([header, fare_rules])
        i += 1

    # carrier_code and have_fare_rules are assumed to be shared by all flights
    return information_flights, carrier_code, bool(fare_rules)


def get_vectorstore_web(carrier_code):
    """Return a vectorstore based on the content of an airline company web portal.

    Parameters:
    carrier_code (str): the IATA code of the airline company

    Return:
    A vectorstore, or none if the scraping could not be performed for some reason.
    """
    webtext = sc.scrape_text_from_iata(carrier_code)
    if webtext:
        return text_to_vector_store(webtext)
    return None


def process_and_display_flight_fares(
    flights_list, llm=llm, embedding_model=embedding_model
):
    """From a flight list (all flights of a given trip), output the vectorstore
    based on all fare rules (from ATPCO), the list of fares to display in the
    chat (filled templated), a boolean stating if there was fare rules in the
    ATPCO database, and the vectorstore based on the trade portal of the company.

    Parameters:
    - flights_list (list): list of flight dictionaries (as formatted by get_fare_rules_from_DB
    and get_fare_rules_from_API)
    - Optional llm (LLM model, e.g. AzureChatOpenAI instance): the language model to be used
    - Optional embedding_model (typically OpenAIEmbeddings instance): the model used to embed the text chunks

    Return:
    tuple: ATPCO based vectorstore, list of fare templates to display, a boolean,
    trade portal based vectorstore
    """

    information_flights, carrier_code, have_fare_rules = format_flight_info(
        flights_list
    )

    vectorstore_web = get_vectorstore_web(carrier_code)

    if not have_fare_rules:
        return None, None, have_fare_rules, vectorstore_web

    chunks_per_flight = []
    for info in information_flights:
        if have_fare_rules:
            chunks_per_flight.append(
                split("FARE RULES FOR " + info[0] + " :\n" + info[1] + "\n\n")
            )
        else:
            chunks_per_flight.append(
                split("NO FARE RULES FOUND FOR " + info[0] + "\n\n")
            )

    fares_to_display = []
    prompt_template = prompt_fill_template.prompt
    question_template = prompt_fill_template.question

    for i in range(len(information_flights)):
        vectorstore = FAISS.from_texts(chunks_per_flight[i], embedding_model)
        chain_template = chain_paragraph(vectorstore, prompt_template, llm=llm)

        filled_template = answer_retrieval_chain(question_template, chain_template)

        fare_to_display = information_flights[i][0] + "\n\n" + filled_template
        fares_to_display.append(fare_to_display)

    chunks_all = []
    for chunks in chunks_per_flight:
        chunks_all += chunks

    vectorstore_all = FAISS.from_texts(chunks_all, embedding_model)

    return vectorstore_all, fares_to_display, have_fare_rules, vectorstore_web
