from langchain.prompts import PromptTemplate


def get_prompt(source=""):
    """Return a prompt to be used for Q&A chains (typically ConversationalRetrievalChain),
    with optional precision of the source.

    Parameters:
    - source (str): the source of the vectorstore that will be used for the Q&A chain

    Return:
    PromptTemplate instance: a Langchain prompt template with inputs names
    "context", "chat_history" and "question" to be used for chain creation
    """
    from_source = "from the " + source if source != "" else ""
    prompt_str = (
        """
        INSTRUCTIONS: Answer the question below accurately based on the provided context """
        + from_source
        + """ in between triple backsticks.
            If the question is about a pdf or a website or portal and the context is not from a PDF
            or website or portal, just output 'Unknown', whatever the question.
            If you don't know the answer from the context, output 'Unknown',
            do not make a sentence.
            Do not try to make up answers.

            """
        + source
        + """CONTEXT: ```{context}```

            CHAT HISTORY: {chat_history}

            USER QUESTION: {question}

            HELPFUL ANSWER: """
    )

    return PromptTemplate(
        input_variables=["context", "chat_history", "question"], template=prompt_str
    )


# Build prompt for the chain used to display key points paragraph from website
prompt_paragraph_web_str = """
    CONTEXT FROM WEBSITE: ```{context}``` \n

    INSTRUCTIONS: {question} \n

    KEY POINTS PARAGRAPH: \n
    """

question_paragraph_web = """You are assisting a travel agent with providing
    a customer with practical and useful information about its reservation conditions:
    change, refund, special situations...

    Your task is to identify and list some key conditions from the website content
    provided to you as a context, and output them into at most 5 clear and
    concise bullet points.

    Pay special attention to exceptional conditions linked to specific events,
    such as covid, sanitary situations, natural disasters.
    """

prompt_paragraph_web = PromptTemplate(
    input_variables=["context", "question"], template=prompt_paragraph_web_str
)


# Build prompt for the chain used to display key points paragraph from pdf file
question_paragraph_PDF = """
    * rules that apply in case of delay, re-routing...
    * specified time limits to take steps or make a claim in case of problems
    * specific tax rules, anything about tax codes
    * exceptional refund or change conditions linked to specific events (covid...)
    * specific situations of the customer
    * conditions involving dates, fees, percentages or figures in general
    """

prompt_paragraph_PDF_str = """
    CONTEXT FROM PDF FILE: ```{context}``` \n

    INSTRUCTIONS: You are assisting a travel agent with retrieving
                useful and technical information about the reservation conditions
                for a specific airline company: change, refund, taxes...

                Your task is to identify and list some practical key rules from the airline
                pdf file provided to you as a context, and output them into at most
                4 clear and concise bullet points.

                Pay special attention to figures and to the following, by order of importance:\n
                {question} \n
                Do not summarize the document, just output some concrete pratical rules
                that apply in some cases (keep it short).

    KEY POINTS PARAGRAPH: \n
    """

prompt_paragraph_PDF = PromptTemplate(
    input_variables=["context", "question"], template=prompt_paragraph_PDF_str
)
