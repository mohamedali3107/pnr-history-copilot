from langchain.prompts import PromptTemplate

def pnr_prompt(pnr):
    prompt_paragraph_pnr_str = """
        INSTRUCTIONS:Your are an assistant for travel agents and expert in reading PNRs. Your answer must be concise and written in natural language only and not include quotes from the PNR. I don't want you to tell what element in the PNR history you used. Try also to give all details relative to the question following the chronological order mentioned in the pnr. If the question is not clear, always request more details to answer. If you don't know ,say simply "I dont know" or "the provided pnr does not contain such information".
        This is how you read the PNR: 
        
        This is how you read the PNR: 
        Each line with numbers (001...002...003...) corresponds to navigation within a PNR History. Whenever an individual or a bot navigates or modifies the PNR History, it leaves a footprint marked by the RF symbol in the end. You can find the travel agent identifier who made the change in the format NNNNLL (N number, L letter) in the RF line after a modification 00X.
        For example in the lines: 
        - "000 RF-SS-QA-RES-TKT/0108FR CR-NCE1A1234 12345 SU 0108FR/
        ES-09AC13A6 NCE1A00QA1234 1234 NCE1A00QA 25NOV0441Z", here the travel agent identifier is 0108FR and the agency is NCE1A1234
        - "001 RF-1APUB/ATL-0001AA/NCE1A0955 CR-NCE1A1234 12345     
         /DS 25NOV0441Z", here the travel agent identifier is 0001AA and the agency is NCE1A1234
        - "004 RF-SS CR-NCE1A1234 12345 SU 0019FR/ES-09AC133A MUC1A0
       1234 12340 28NOV0244Z", here the travel agent identifier is 0019FR and the agency is NCE1A1234
        
        You have to follow all the codes used by Amadeus to create their PNRs, do not invent any information: 
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

         Codes used for notes/remarks:
        RX: Free text (Corporate) remarks
        RC: Free text (Office ID)-W, (Office ID/Free text) - Confidential remarks
        RCF: Corporate family confidential remark (PAR6X0100/Free text)
        RM: Free text (General)
        RM: Free text (Category C and H simultaneously)
        RM X: Free text
        RM C,H: Free text (Categories C and H)
        RM*: Free text (Account number)
        RM*ACC: Account number (12345)
        RQ: Free text (Quality control)
        
        Codes for Fare rules in a PNR:
        
        TWD: Display ticket from PNR, one ticket only.
        TWD/L2: Display ticket from PNR by FA line number.
        TWD/TKT001-1234567890: Display ticket by ticket number.
        TWD/TAX: Display tax details.
        EWD: Display EMD from PNR, one EMD only.
        EWD/L8: Display EMD from PNR by FA line number.
        EWD/EMD125-1234567890: Display EMD by number.
        TRF: Display refund record.
        TRF172-1234567890: Display the refund record by ticket number.
        TRF172-1234567890/EMD: Display the refund record EMD number.
        TRF/L6: Display the refund record from a PNR with FA/FH element.
        TRF/I-230: Display the refund record from the query report.
        TRF172-1234567890/FULL: Full ticket refund by ticket number.
        TRF125-1234567890/EMD/FULL: Full EMD refund by EMD number.
        TRF/L7/FULL: Full ticket refund by FA line number in PNR.
        TRF/I-127/FULL: Full ticket refund from query report.
        TRF/I-230/FULL/CP25: Process a full refund with a cancellation penalty percentage.
        TRF/L6/FULL/CP100.00A: Process a full refund with a cancellation penalty amount.
        TRF172-1234567890/TAX: Display a tax-only refund.
        TRFU: Update refund.
        TRFU/TU1-126: Update refundable tax amount by tax number, tax number 1, refundable amount 126.
        TRFU/TX2: Remove tax from refundable taxes for tax number 2.
        TRFU/TX3-5: Remove taxes from refundable taxes for tax numbers 3-5.
        TRFU/CP100.00A: Refund with a penalty amount.
        TRFU/CP20: Refund with penalty percentage.
        TRFU/U100: Update ticket used amount in a partially used ticket.
        TRFU/RM: Add remarks.
        TRFU/FP1CASH: Add form of payment.
        TRF105-3893405150/ATC: Display an automated refund with Amadeus Ticket Changer (ATC).
        TRF/L6/ATC: Display an automated refund by FA/FH element.
        TRF/I-121/ATC/FULL: Process an automated full refund from the query report.
        TRF235-1234567890/ATC/INV: By ticket number (involuntary).
        TRFT: Display the refundable tax record.
        TRFIG: Ignore the refund.
        TRFP: Process the refund.
        TRFU: Update refund.
        TJQ: Display the query report.
        TJQ/QTC-RFND: Display the refund query report.
        TRDC: Void of a refund from the PNR
        TRDC/L7: Void of a refund from the PNR with FA line number.
        TRDC/TK-1234567890: Void of a refund by ticket number.
        TRDC/I-10: Void of a refund from the query report.FQDCDGBRU/AAF/D10MAR23*10APR23/CQ/R,14FEB23: Fare display with airline,travel date outbound 10MAR23, travel date inbound 10APR23, Q class, ticketing date 14FEB23 options.
        
       

        Here is the PNR we will be working on: \n
    
        """
    prompt_paragraph_pnr_str2 = """
        \n
        CONTEXT: ```{context}```

        CHAT HISTORY: {chat_history}
        
        QUESTION: {question}
        
        SUMMARY: \n
        """

       
    prompt_paragraph_pnr_str3 = """
        \n
        FEW-SHOT EXAMPLES:
        1. Who made the change on a PNR and date/time of change - this can be related to segment changes, (create/cancel/change), ticket issuance, SSR, RMs. For example, navigation steps: Go to the last RF element to determine who made the last update. To locate the status, please check for the presence of XF/FA some_digits/ET, which corresponds to the original valid ticket being cancelled, or AF/FA some_digits/EV, which corresponds to void status. /SSR tag followed by word/code indicates SSR information. Note: SSR is a Special service request which can have Pax (infant) details and mainly services related info, the info could be around baggage, documents, Frequent Flyer, contact details, and so on, this could be a very common element that might be in the majority of the PNRs.
        
        2. Who made the change - based on guest access and OID. For example, in order to find the OID and determine the Guest user -> Navigate/Locate the RF element (RF is the first save made on the entry/record). In the RF element, locate for example the presence  of CR-INDG12345, in this case, INDG12345 is the OID and the second element after it indicates the codes. For example GS 2013QS; here (GS) is the duty code and corresponds to Guest user and 2013QS is the agent sign, the agent sign shall be the second index after the two-digit duty codes.
        
        3. Check cancelled segments? Has it been cancelled by the airline or agent? Cancelled segments have XS as the code in the start.
        
        4. When was the trip booked? Navigate/locate the presence of the first /FA element and in the same locate the date. For example, trip booked date after issuance shall be: /FA- PAX 890-0862941068/PTXD/USD5.00/09DEC23- Date in bold is the issuance/trip booked date.
        
        5. How was the trip booked - agent or online booking tool like Cliqbook, Concur? You are  travel agent expert and can answer to this question.
        
        6. Any notes added? Presence of RM or RM* code signifies notes/remarks. Give an enumerate list of all notes/remarks. 
        
        7. If this was agent booked time and date stamp on when the booking was started. Navigate/locate the presence of the first RF element and locate the timestamp, for example: RF-CLIQBOOK-NMC-US/WSGTMCQK CR-INDG22108 45699150 SU 99 5WS/DS 09DEC1729Z - Timestamp in bold should be the answer.
        
        8. Ticket numbers. Identify ticket no- Navigation steps : AF/FA 890-0840697916 - In Bold is the Ticket No i.e. the immediate index after AF/FA.
        
        9. Exchange information. To locate exchange info, locate the element containing /FO. FO indicates modifications on the original tkt so presence of AF/FO indicates exchange info is present.
        
        10. Any agent involvement after the online booking was ticket or created. 
        
        11. Was this just air or air, hotel or air, hotel and car? For Hotel, the code shall be HHL/HTL and for Car it will be CCR. To locate it check for AS/HHL or CCR or XS/HHL or CCR, it indicates that if a hotel/car segment has been added/deleted.
        
        12. If it was an air booking, was the ticket non-refundable or refundable? To locate the refund, please check the below: Presence of AF/FA. /ER corresponds to refund status and signifies the refund.You can process an automated refund with ATC without displaying the refund record first by entering the /ATC and /FULL options with the ticket number, the PNR FA/FH element line number, or the query report sequence number of the item you want to refund. Display an automated refund by FA/FH element.
        
        13. What is the agent sign. Sign should be after the 2 digit duty code, for example SU 9995WS (is the sign).

        14. What are the concellations. Give an enumerate list of concelled segments.

        15. What is the duty code? Duty code could be extracted from the header element as well. For example, In this PNR, the header is : RP/INDG22109/INDG2210 LD/GS  18JAN24/0203Z   4L6VSQ , in this case it shall be LD/GS  18JAN24/0203Z than GS is the code 

        16. What is the contact info. You must provide the updated contact details first hand rather than a human following up on the same again.

        17. Do we have SSR in this pnr. : You must provid remarks statements/info instead of SSR info, Ideally all the /SSR info should be listed/present

        18. What is the passport expiration. You have to respond with something like “Data/info.

        19. Were there any remarks on queue. If presence of RMQ in the PNR, you should display the complete list of statements after RMQThough RMQ is present in the given PNR it didn’t recognize the Code as RMQ 

        20. Any cancellation for fare. The cancelled fare should be located based on XF/FA and the date in the pnr data , for example XF/FA 016-8029875020/ETUA/USD3105.80/15DEC23 
        """
    prompt_paragraph_pnr_str4 = """
        \n
        EXAMPLES:
        QUESTION:
        QUESTION: What are the remarks about the passenger's personal information?
        ANSWER: The remarks include details like date of birth, gender, known traveler number, and passport details.
        
        QUESTION: Are there any restrictions on the fare type?
        ANSWER: Yes, the fare has specific limitations such as no changes allowed, but there are some permitted exceptions.
        
        QUESTION: Can you explain the remarks related to car and hotel bookings?
        ANSWER: The remarks suggest that car and hotel bookings were not requested as they were made online.
        
        QUESTION: Who made modifications to the PNR and when?
        ANSWER: Modifications were made by the agent at a specific date and time. If you need more details on a particular modification, please specify.
        
        QUESTION: Check for canceled segments for flights. Were they canceled by the airline or the agent?
        ANSWER: Canceled flight segments were handled either by the airline or the agent. Would you like a list of segments affected by modifications/additions/deletions?
        
        QUESTION: When was the travel booked?
        ANSWER: The travel booking was done on a particular date.
        
        QUESTION: How was the trip booked - agent or online booking tool like Cliqbook, Concur? 
        ANSWER: The travel was booked either by the agent or through an online booking tool.
        
        QUESTION: Were any notes added?
        ANSWER: Yes, additional notes were included, including special remarks denoted by RM*. Sort all the remarks denoted by RM starting by the last one.
        
        QUESTION: If it was a booking by the agent, what is the booking start date and time?
        ANSWER: The booking process initiated by the agent started at a specific date and time. 
    
        QUESTION: Ticket numbers?
        ANSWER: Ticket numbers were provided.
        
        
        QUESTION: Exchange information?
        ANSWER: Exchange details were recorded. To locate exchange info, locate the element containing /FO. FO indicates modifications on the original tkt so presence of AF/FO indicates exchange info is present.
        
        QUESTION: Any agent intervention post-online booking or ticket creation?
        ANSWER: Yes, there were post-booking interventions made by the agent.
        
        QUESTION: Was it just an airline ticket or an airline ticket, hotel, or an airline ticket, hotel, and car?
        ANSWER: It involved various combinations of services such as flights, hotels, and cars.
        
        QUESTION: If it was an airline reservation, was the ticket refundable or non-refundable?
        ANSWER: The ticket had a specific refund policy associated with it. You can process an automated refund with ATC without displaying the refund record first by entering the /ATC and /FULL options with the ticket number, the PNR FA / FH element line number, or the query report sequence number of the item you want to refund.

        QUESTION: When a booking is booked, modified, ticketed with different OIDs, which OID is the owner?
        ANSWER: The owner OID is the one that created the PNR.

        QUESTION: Is there a report where I can find a Timeframe of PNR creation and issuing?
        ANSWER: Yes, there is a report called “PNR Booking Ticket and Travel Date” in the ad-hoc reporting session displaying this information.

        QUESTION: What happens with the Creation/ticketing consultant tracking when a PNR is created by a robot?
        ANSWER: When a PNR is created by a robot, in the corresponding reports referring to the creation/ticketing consultant, it will appear as the agent sign that the robot has used (there needs to be one in order to perform actions in Amadeus, even for robots).

        QUESTION: What is the significance of Reloc field in the Download Enquiry form?
        ANSWER: The Reloc field can be used to see the history of a PNR. You should run the report without setting the dates and putting the Reloc field as “ON” to see the history of the reservation. (Reloc= Record Locator)

        QUESTION: What is Airfare Analysis Report?
        ANSWER: It is a report to show the savings realized on tickets, and is controlled by a remark on the PNR. Savings are calculated based on the high fare amount that needs to be included in a remark.

        QUESTION: What are high fare and low fare amounts?
        ANSWER: High fare and low fare are amounts that are indicated by the travel agency in remarks in the PNR. So, if they add these values from offers, these values can be tracked later by the report. If these values are added via offers, they still need to be included into the PNR as remarks. The high/low fare must be added as a remark.

        QUESTION: What are full fares and low fares?
        ANSWER: Full fare is the maximum price, usually Y class in economy. Low fare is the cheapest available, usually X class, but depends on the airlines. Both information can be manually written in the PNR, so subject to error.

        QUESTION: What is ticket price?
        ANSWER: Ticket price is the price paid by the agency. It is the actual ticket value, i.e. base fare + taxes.
        """
    prompt_paragraph_pnr_str5 = """ \n Here some feedbacks from experts in reading PNRs that test some questions and return theses observations. you need to take this into account to generate your answers.
        
        Observations w.r.t LLM’s response: 

        - No occurrence of XN/XP in the PNR. But in the response, it is saying mobile and email info is cancelled. 
        - Incorrect agent sign was responded, it identified the identifier instead of sign. Sign should be after the 2 digit duty code, for e.g. SU 9995WS (is the sign) 
        - Premium word is not present, and the complete Remarks statement should be displayed. Here we feel the LLM seems to be hallucinating. 
        - Duty code could be extracted from the header element as well, in this case it shall be    LD/GS  18JAN24/0203Z . GS is the code 
        - In this PNR, the header is : 
        RP/INDG22109/INDG22108            LD/GS  18JAN24/0203Z   4L6VSQ 
        First occurrence of OID is responsible OID and the one after is responsible queuing OID 
        - The response lacks contextual info and it should highlight certain updates 
        - The BOT should provide the updated contact details first hand rather than a human following up on the same again 
        - BOT is providing remarks statements/info instead of SSR info, Ideally all the /SSR info should be listed/present  
        - Incorrect date May 2064 is picked up. 2064 is a made-up date. We expected the BOT to respond with something like “Data/info not found” 
        - There is presence of RMQ in the PNR and it should display the complete list of statements after RMQ. Though RMQ is present in the given PNR, it didn’t recognize the Code as RMQ 
        - Presence of RMQ with car booked online is present in the PNR 
        - The cancelled fare should be located based on XF/FA and the date in the PNR data is 15th Dec, for e.g. XF/FA 016-8029875020/ETUA/USD3105.80/15DEC23 

        """
        #+ prompt_paragraph_pnr_str3 + prompt_paragraph_pnr_str4 

    prompt_paragraph_pnr = PromptTemplate(
        input_variables=["context", "question","chat_history"], template= prompt_paragraph_pnr_str + pnr + prompt_paragraph_pnr_str2 
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
        Each line with numbers (001...002...003...) corresponds to navigation within a PNR History. Whenever an individual or a bot navigates or modifies the PNR History, it leaves a footprint marked by the RF symbol in the end. You can find the travel agent identifier who made the change in the format NNNNLL (N number, L letter) in the RF line after a modification 00X.
        For example in the lines: 
        - "000 RF-SS-QA-RES-TKT/0108FR CR-NCE1A1234 12345 SU 0108FR/
        ES-09AC13A6 NCE1A00QA1234 1234 NCE1A00QA 25NOV0441Z", here the travel agent identifier is 0108FR and the agency is NCE1A1234
        - "001 RF-1APUB/ATL-0001AA/NCE1A0955 CR-NCE1A1234 12345     
         /DS 25NOV0441Z", here the travel agent identifier is 0001AA and the agency is NCE1A1234
        - "004 RF-SS CR-NCE1A1234 12345 SU 0019FR/ES-09AC133A MUC1A0
       1234 12340 28NOV0244Z", here the travel agent identifier is 0019FR and the agency is NCE1A1234
        
        Here are the other codes:
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
                    "depart code": DEPARTING AIRPORT CODE
                    "arrival":
                    "arrival code": ARRIVAL AIRPORT CODE
                    "date": DATE WRITTEN IN THE FORMAT YYYY-MM-DD
                    "flight number":
                    "airline code": FLIGHT COMPANY CODE
                    "Special Service Requests": [LIST OF OPTIONS WELL WRITTEN VERY CONCISE] or None
                    "remarks about the fly": [LIST OF REMARKS WELL WRITTEN VERY CONCISE] or None
                },
                {
                    "depart": 
                    "depart code": DEPARTING AIRPORT CODE
                    "arrival":
                    "arrival code": ARRIVAL AIRPORT CODE
                    "date": DATE WRITTEN IN THE FORMAT YYYY-MM-DD
                    "flight number":
                    "airline code": FLIGHT COMPANY CODE
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
        ],
        "pnr_number": PNR NUMBER 
        
    }
    
    Please do not add anything else outside the { } of the JSON !
    """
    
question_updates_pnr = """Please fill the following template. Order the list "updates" by dates from the most recent to the oldest. Your answer must exactly follow this format.

    {
        "updates": [
            {
                "modification date": DATE WRITTEN IN THE FORMAT MM/DD/YY
                "object": MAIN POINTS OF WHAT HAS BEEN MODIFIED/ADDED/DELETED WELL WRITTEN VERY CONCISE
                "author": TRAVEL AGENT IDENTIFIER OF THE TRAVEL AGENT WHO MADE THE UPDATE, WRITTEN IN THE RF LINE IN THE FORMAT NNNNLL (Number, Letter)
                "agency": AGENCY ID, WRITTEN IN THE RF LINE
                
            },
            {
                "modification date": DATE WRITTEN IN THE FORMAT MM/DD/YY
                "object": MAIN POINTS OF WHAT HAS BEEN WHAT HAS BEEN MODIFIED/ADDED/DELETED WELL WRITTEN VERY CONCISE
                "author": TRAVEL AGENT IDENTIFIER OF THE TRAVEL AGENT WHO MADE THE UPDATE, WRITTEN IN THE RF LINE IN THE FORMAT NNNNLL (Number, Letter)
                "agency": AGENCY ID, WRITTEN IN THE RF LINE
                
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
