from langchain.prompts import PromptTemplate

def pnr_prompt(pnr):
    prompt_paragraph_pnr_str = """
        INSTRUCTIONS: I want you to be an assistant for travel agents and help them with PNRs. Your answer must be concise and written in natural language only and not include quotes from the PNR. I don't want you to tell what element in the PNR history you used. 
        This is how you read the PNR: 
        
        Each line with numbers (001...002...003...) corresponds to navigation within a PNR History. Whenever an individual or a bot navigates or modifies the PNR History, it leaves a footprint marked by the RF symbol in the end. For instance, in the line RF-NMC-US/WSGTMFLS, WSGTMFLS is the identifier of the person. 
        Here are additionnal codes: 
        Code used for creating a PNR (Passenger Name Record):
        EO	Origin ETR
        FO	Financial element origin
        KO	Original general (RM) or confidential (RC) remarks
        MO	Origin MCO
        OB	Origin billing address (AB)
        OD	Original postal address (AM)
        OE	Origin security (ES)
        OF	Origin fare
        OI	Amadeus original insurance
        OK	Origin keyword (SK)
        OM	Origin marriage segments
        ON	Origin name (NM)
        OO	Origin OSI
        OP	Origin phone (AP)
        OQ	Origin option (OP)
        OR	Origin SSR
        OS	Origin flight segment
        OT	Original ticket disposition (TK)
        OY	Origin total price
        QO	Original address verification
        RO	Origin reservation number
        TO	Original attachment

        Codes used for adding elements to a PNR:
        AB	Added billing address
        AE	Added individual security
        AF	Added fare
        AI	Added Amadeus insurance
        AK	Added special keyword
        AM	Added mail address
        AN	Added name element, passenger type code, or identification
        AO	Added option
        AP	Added phone
        AQ	Added address verification
        AR	Added general or confidential remarks
        AS	Added element containing status code (except SSR)
        AT	Added ticket disposition
        AY	Added Amadeus insurance total price
        EA	Added ETR
        FA	Added financial element
        GM	Added marriage
        MA	Added miscellaneous service fees (MCO)
        OA	Added OSI
        RA	Added reservation number
        SA	Added SSR
        TA	Added attachment

        Codes used for modifying elements in a PNR:
        CB	Modified billing address
        CE	Modified individual security
        CF	Modified fare
        CM	Modified mail address
        CN	Modified name element, passenger type code, or identification
        CO	Modified option
        CP	Modified contact
        CQ	Modified address verification
        CR	Modified remarks
        CS	Modified status code
        CT	Modified ticketing arrangement
        CW	Modified waitlist priority
        CY	Modified Amadeus insurance total price
        EC	Modified ETR
        FC	Modified financial post element
        OC	Modified OSI
        RP	Modified responsible agency

        Codes used for canceling or deleting elements in a PNR:
        EX	Canceled ETR
        FX	Canceled financial post
        MX	Canceled MCO
        OX	Canceled OSI
        RX	Canceled reservation number
        SX	Canceled SSR
        TX	Canceled attachment
        XB	Canceled mail forwarding address
        XE	Canceled individual security
        XF	Canceled fare
        XI	Canceled Amadeus insurance
        XK	Canceled special keyword
        XM	Canceled mail forwarding address
        XN	Canceled name
        XO	Canceled option
        XP	Canceled phone
        XQ	Canceled address verification
        XR	Canceled general or confidential remark
        XS	Canceled element containing status code (except SSR)
        XT	Canceled ticket issuance disposition
        XY	Canceled Amadeus insurance total price
        DL	Deleted element
        DM	Deleted marriage segment

        Other codes:
        IS	Increase the number of people in the group
        MC	MCO element or modified XSB segment
        NT	Transmitted names (groups only)
        QA	Automatic call file placement
        QU	Call file update
        RF	Received from
        RR	PNR replication (RRA)
        SP	PNR split
        SR	Refused SSR
        TC	Flight time change
        
        
        Here is the PNR we will be working on: \n
        """
    prompt_paragraph_pnr_str2 = """
        \n
        CONTEXT: ```{context}```

        CHAT HISTORY: {chat_history}
        
        QUESTION: {question}
        
        SUMMARY: \n
        """
    prompt_paragraph_pnr = PromptTemplate(
        input_variables=["context","chat_history", "question"], template= prompt_paragraph_pnr_str + pnr + prompt_paragraph_pnr_str2
    )
    return prompt_paragraph_pnr


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

# Build prompt for the chain used to display summary of a pnr

def prompt_summary_pnr(pnr):
    prompt_paragraph_pnr_str = """
        INSTRUCTIONS: I want you to be an assistant for travel agents and help them with PNRs. Your answer must be concise and written in natural language only and not include quotes from the PNR. I don't want you to tell what element in the PNR history you used. 
        This is how you read the PNR: 

        This 
        Code used for creating a PNR (Passenger Name Record):
        EO	Origin ETR
        FO	Financial element origin
        KO	Original general (RM) or confidential (RC) remarks
        MO	Origin MCO
        OB	Origin billing address (AB)
        OD	Original postal address (AM)
        OE	Origin security (ES)
        OF	Origin fare
        OI	Amadeus original insurance
        OK	Origin keyword (SK)
        OM	Origin marriage segments
        ON	Origin name (NM)
        OO	Origin OSI
        OP	Origin phone (AP)
        OQ	Origin option (OP)
        OR	Origin SSR
        OS	Origin flight segment
        OT	Original ticket disposition (TK)
        OY	Origin total price
        QO	Original address verification
        RO	Origin reservation number
        TO	Original attachment

        Codes used for adding elements to a PNR:
        AB	Added billing address
        AE	Added individual security
        AF	Added fare
        AI	Added Amadeus insurance
        AK	Added special keyword
        AM	Added mail address
        AN	Added name element, passenger type code, or identification
        AO	Added option
        AP	Added phone
        AQ	Added address verification
        AR	Added general or confidential remarks
        AS	Added element containing status code (except SSR)
        AT	Added ticket disposition
        AY	Added Amadeus insurance total price
        EA	Added ETR
        FA	Added financial element
        GM	Added marriage
        MA	Added miscellaneous service fees (MCO)
        OA	Added OSI
        RA	Added reservation number
        SA	Added SSR
        TA	Added attachment

        Codes used for modifying elements in a PNR:
        CB	Modified billing address
        CE	Modified individual security
        CF	Modified fare
        CM	Modified mail address
        CN	Modified name element, passenger type code, or identification
        CO	Modified option
        CP	Modified contact
        CQ	Modified address verification
        CR	Modified remarks
        CS	Modified status code
        CT	Modified ticketing arrangement
        CW	Modified waitlist priority
        CY	Modified Amadeus insurance total price
        EC	Modified ETR
        FC	Modified financial post element
        OC	Modified OSI
        RP	Modified responsible agency

        Codes used for canceling or deleting elements in a PNR:
        EX	Canceled ETR
        FX	Canceled financial post
        MX	Canceled MCO
        OX	Canceled OSI
        RX	Canceled reservation number
        SX	Canceled SSR
        TX	Canceled attachment
        XB	Canceled mail forwarding address
        XE	Canceled individual security
        XF	Canceled fare
        XI	Canceled Amadeus insurance
        XK	Canceled special keyword
        XM	Canceled mail forwarding address
        XN	Canceled name
        XO	Canceled option
        XP	Canceled phone
        XQ	Canceled address verification
        XR	Canceled general or confidential remark
        XS	Canceled element containing status code (except SSR)
        XT	Canceled ticket issuance disposition
        XY	Canceled Amadeus insurance total price
        DL	Deleted element
        DM	Deleted marriage segment

        Other codes:
        IS	Increase the number of people in the group
        MC	MCO element or modified XSB segment
        NT	Transmitted names (groups only)
        QA	Automatic call file placement
        QU	Call file update
        RF	Received from
        RR	PNR replication (RRA)
        SP	PNR split
        SR	Refused SSR
        TC	Flight time change
        
        
        Here is the PNR we will be working on: \n
        """
    prompt_paragraph_pnr_str2 = """
        \n
        CONTEXT: ```{context}```
        
        QUESTION: {question}
        
        SUMMARY: \n
        """
    prompt_paragraph_pnr = PromptTemplate(
        input_variables=["context", "question"], template= prompt_paragraph_pnr_str + pnr + prompt_paragraph_pnr_str2
    )
    return prompt_paragraph_pnr

question_paragraph_pnr = """
    Clearly provide me with a concise summary of the PNR. For the cities, please provide me the whole name and not an abbrevation. Please put as many flights and updates as there are in the PNR History.
    Your answer must follow exactly this json format: 
    {   "summary": {
            "passengers name": [LIST OF PASSENGERS],
            "flights": [
                {
                    "depart": 
                    "arrival":
                    "date": DATE WRITTEN IN THE FORMAT MM/DD/YY
                    "flight number":
                    "Special Service Requests": [LIST OF OPTIONS WELL WRITTEN VERY CONCISE] or None
                    "remarks about the fly": [LIST OF REMARKS WELL WRITTEN VERY CONCISE] or None
                },
                {
                    "depart": 
                    "arrival":
                    "date":
                    "flight number":
                    "Special Service Requests": [LIST OF OPTIONS WELL WRITTEN VERY CONCISE] or None
                    "remarks about the fly": [LIST OF REMARKS WELL WRITTEN VERY CONCISE] or None
                }
            ],
            "ticket numnber": [LIST OF TICKET NUMBER],
            "general remarks": [LIST OF REMARKS RANKED BY RELEVANCE FOR A TRAVEL AGENT]
        }, 
        "updates": [
            {
                "modification date": DATE WRITTEN IN THE FORMAT 12 Oct 2022
                "object": MAIN POINTS OF WHAT HAS BEEN MODIFIED/ADDED/DELETED WELL WRITTEN VERY CONCISE
                "author": AUTHOR OF THE UPDATE 
            },
            {
                "modification date": DATE WRITTEN IN THE FORMAT 12 Oct 2022
                "object": MAIN POINTS OF WHAT HAS BEEN WHAT HAS BEEN MODIFIED/ADDED/DELETED WELL WRITTEN VERY CONCISE
                "author": AUTHOR OF THE UPDATE 
            }
        ]
        
    }
    
    Please do not add anything else outside the { } of the JSON !
    """
    
question_updates_pnr = """Please fill the following template. Order the list "updates" by dates from the most recent to the oldest. Your answer must exactly follow this format.

    {
        "updates": [
            {
                "modification date": DATE WRITTEN IN THE FORMAT MM/DD/YY
                "object": MAIN POINTS OF WHAT HAS BEEN MODIFIED/ADDED/DELETED WELL WRITTEN VERY CONCISE
                "author": AUTHOR OF THE UPDATE 
            },
            {
                "modification date": DATE WRITTEN IN THE FORMAT MM/DD/YY
                "object": MAIN POINTS OF WHAT HAS BEEN WHAT HAS BEEN MODIFIED/ADDED/DELETED WELL WRITTEN VERY CONCISE
                "author": AUTHOR OF THE UPDATE 
            }
        ]
    }

    Do not add anything else outside the { } of the JSON
    """
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
