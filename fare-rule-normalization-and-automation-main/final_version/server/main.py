from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import (
    CORSMiddleware,
)
from fastapi import Body
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain

# Custom imports
import functions.get_fare_rules_from_API as gfAPI
from functions.get_fare_rules_from_DB import get_fare_rules_from_DB
from functions.process_and_display_fares import process_and_display_flight_fares
from functions.answer_chat import answer
from functions.create_qa_chain import create_qa_chain, chain_paragraph, create_qa_chain_no_context, chain_paragraph_pnr
from functions.generate_prompt import get_prompt, pnr_prompt
from functions.generate_prompt import prompt_paragraph_web, question_paragraph_web
from functions.generate_prompt import prompt_paragraph_PDF, question_paragraph_PDF
from functions.generate_prompt import prompt_summary_pnr, question_paragraph_pnr, question_updates_pnr
import utils.utils as u
import uuid
from typing import Dict

# Initiate APP
app = FastAPI()

# CORS - Origins (These are the origins that are allowed to access the backend)
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:4174",
    "http://localhost:3000",
    "http://localhost:8000",
]

# CORS - Middleware (This is to allow the frontend to access the backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatSession():
    qa_chain_PNR : ConversationalRetrievalChain
    qa_chain_ATPCO : ConversationalRetrievalChain
    qa_chain_PDF : ConversationalRetrievalChain
    qa_chain_WEB : ConversationalRetrievalChain
    chat_history : ConversationBufferMemory

    def __init__(self):
        self.qa_chain_PNR = None
        self.qa_chain_ATPCO = None
        self.qa_chain_PDF = None
        self.qa_chain_WEB = None
        self.chat_history = ConversationBufferMemory(memory_key="chat_history", output_key="answer")

    def __str__(self):
        string = "QA Chain : \n"
        string += str(self.qa_chain_PNR)
        string += str("\nChat History : \n")
        string += str(self.chat_history)
        string += str("\n")
        return string

global sessions
sessions : Dict[int, ChatSession] = dict()

# Get bot response
@app.post("/answer_chat")
async def get_answer(question: str = Body(..., embed=True), session_id: str = Body(..., embed=True),):
    print("Session : ", session_id)
    print(sessions[session_id])

    response = answer(question, sessions[session_id].qa_chain_PNR)
    #response = answer(question, sessions[session_id].qa_chain_ATPCO)

    # if response == "Unknown":
    #     response = answer(question, sessions[session_id].qa_chain_PDF)

    # if response == "Unknown":
    #     response = answer(question, sessions[session_id].qa_chain_WEB)

    if response == "Unknown":
        response = "Please upload a PNR History first."

    print({"answer": response})

    return {"answer": response}

# This function takes as input the departure date, the origin code, the destination code and the airline code
@app.post("/fill_template_API")
async def fill_template(
    departure_date: str = Body(..., embed=True),
    origin_code: str = Body(..., embed=True),
    destination_code: str = Body(..., embed=True),
    airline_code: str = Body(..., embed=True),
    session_id: str = Body(..., embed=True),
):
    origin_code = origin_code.upper()
    destination_code = destination_code.upper()
    airline_code = airline_code.upper()

    fare_rules_list = gfAPI.get_fare_rules_from_API(
        origin_code, destination_code, airline_code, departure_date
    )
    if fare_rules_list is None:
        return {"API_error": True}

    (
        vector_store_ATPCO,
        fares_to_display,
        have_fare_rule,
        vector_store_WEB,
    ) = process_and_display_flight_fares(fare_rules_list)

    if have_fare_rule:
        prompt = get_prompt(source="ATPCO")
        sessions[session_id].qa_chain_ATPCO = create_qa_chain(vector_store_ATPCO, sessions[session_id].chat_history, prompt)

    prompt = get_prompt(source="Webtext")
    #global qa_chain_WEB

    have_webtext, paragraph_webtext = False, "nothing"
    if vector_store_WEB:
        sessions[session_id].qa_chain_WEB = create_qa_chain(vector_store_WEB, sessions[session_id].chat_history, prompt)
        chain_paragraph_web = chain_paragraph(
            vector_store_WEB, prompt_paragraph_web, nb_chunks=10
        )
        have_webtext = True
        # prompt_paragraph = "You are a travel agent assistant, give me 3 useful information included in this webpage in bullet points."
        paragraph = chain_paragraph_web({"query": question_paragraph_web})["result"]
        paragraph_webtext = {
            "paragraph": f"Key points retrieved from the web page :\n {paragraph}"
        }

    return {
        "fares_to_display": fares_to_display,
        "have_fare_rule": have_fare_rule,
        "have_webtext": have_webtext,
        "paragraph_webtext": paragraph_webtext,
    }


@app.post("/fill_template_DB")
async def fill_template_from_DB(
    flight_number: str = Body(..., embed=True),
    session_id : str = Body(..., embed=True),
):
    flight_number = flight_number.upper()
    fare_rules_list = get_fare_rules_from_DB(flight_number)

    if fare_rules_list == []:
        return {"DB_error": True}

    (
        vector_store_ATPCO,
        fares_to_display,
        have_fare_rule,
        vector_store_WEB,
    ) = process_and_display_flight_fares(fare_rules_list)

    if have_fare_rule:
        prompt = get_prompt(source="ATPCO")
        #global qa_chain_ATPCO
        sessions[session_id].qa_chain_ATPCO = create_qa_chain(vector_store_ATPCO, sessions[session_id].chat_history, prompt)

    prompt = get_prompt(source="Webtext")
    #global qa_chain_WEB
    have_webtext, paragraph_webtext = False, "nothing"
    if vector_store_WEB:
        sessions[session_id].qa_chain_WEB = create_qa_chain(vector_store_WEB, prompt)
        have_webtext = True
        chain_paragraph_web = chain_paragraph(
            vector_store_WEB, prompt_paragraph_web, nb_chunks=15
        )
        have_webtext = True
        # prompt_paragraph = "You are a travel agent assistant, give me 3 useful information included in this webpage in bullet points."
        paragraph = chain_paragraph_web({"query": question_paragraph_web})["result"]
        paragraph_webtext = {
            "paragraph": f"Key points retrieved from the web page :\n{paragraph}"
        }

    return {
        "fares_to_display": fares_to_display,
        "have_fare_rule": have_fare_rule,
        "have_webtext": have_webtext,
        "paragraph_webtext": paragraph_webtext,
        "DB_error": False,
    }


@app.post("/upload_pdf")
async def upload_pdf(pdf: UploadFile, session_id : str = Body(..., embed=True),):
    pdf = await pdf.read()
    vector_store_PDF = u.pdf_to_vector_store(pdf)
    prompt = get_prompt(source="PDF")
    #global qa_chain_PDF
    print("prompt : ", prompt)
    sessions[session_id].qa_chain_PDF = create_qa_chain(vector_store_PDF, sessions[session_id].chat_history, prompt)
    chain_paragraph_PDF = chain_paragraph(
        vector_store_PDF, prompt_paragraph_PDF, nb_chunks=12, search_type="similarity"
    )

    # prompt_paragraph = "You are a travel agent assistant, give me 3 useful information included in this PDF in bullet points."
    # paragraph = answer(prompt_paragraph, qa_chain_PDF)
    paragraph = chain_paragraph_PDF({"query": question_paragraph_PDF})["result"]
    return {"paragraph": f"Some key points retrieved from the PDF :\n{paragraph}"}

@app.post("/upload_pnr")
async def upload_pnr(pnr: UploadFile):
    session_id = str(uuid.uuid4())
    global sessions
    sessions[session_id] = ChatSession()
    print("New session : ", session_id)
    pnr= await pnr.read()
    pnr_str= pnr.decode("utf-8")
    prompt = pnr_prompt(pnr_str) 
    vector_store_null = u.pdf_to_vector_store(None)
    #chat_history = ConversationBufferMemory(memory_key="chat_history", output_key="answer")
    # qa_chain_PNR= create_qa_chain_no_context(chat_history, prompt)
    # prompt_paragraph_pnr = prompt_summary_pnr(pnr)
    # chain_pnr = chain_paragraph_pnr(prompt_paragraph_pnr)
    # paragraph = chain_pnr({"query": question_paragraph_PDF})["result"]
    # return {"paragraph": f"Summary of PNR history :\n{paragraph}"}
    prompt_paragraph_pnr = prompt_summary_pnr(pnr_str)
    print("Prompt créé")
    print("prompt :", prompt)
    sessions[session_id].chat_history.clear()
    sessions[session_id].qa_chain_PNR = create_qa_chain(vector_store_null, sessions[session_id].chat_history, prompt)
    print("Chaine créée")
    chain_paragraph_pnr = chain_paragraph(
        vector_store_null, prompt_paragraph_pnr, nb_chunks=12, search_type="similarity"
    )
    # chain_update_pnr = chain_paragraph(
    #     vector_store_null, prompt_paragraph_pnr, nb_chunks=12, search_type="similarity"
    # )
    paragraph = chain_paragraph_pnr({"query": question_paragraph_pnr})["result"]
    return {"paragraph": paragraph, "session_id" : session_id}
    #Autre solution: Changer juste le prompt de tous les trucs pour les adapter au pnr
    
