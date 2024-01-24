from langchain.prompts import PromptTemplate

prompt_template_str = """
    CONTEXT: ```{context}``` \n

    INSTRUCTIONS: {question} \n

    FILLED TEMPLATE: \n
    """

template_to_fill = """
TEMPLATE:
Changes condition before departure: EUR value \n
Changes condition no show at first flight: EUR value \n
Changes condition after departure: EUR value \n
Changes condition no show at subsequent flight: Allowed, Not allowed, or Not applicable \n
Refund condition for cancellation before departure: Allowed, Not allowed, or Not applicable \n
Refund condition no show at first flight: Allowed, Not allowed, or Not applicable \n
Refund condition no show after departure: Allowed, Not allowed, or Not applicable \n
Refund condition no show at subsequent flight: Allowed, Not allowed, or Not applicable \n
"""

question = (
    """Your task is to fill the template below
accurately with the information from the provided context.
Output only the filled template, with the exact same format.
\n If some conditions are applicable
at "ANY TIME", it means that they apply before and after departure.
You may fill the charge fee in whatever currency you find in the
source context (e.g. : EUR, USD, AED...).\n
"""
    + template_to_fill
)

prompt = PromptTemplate(
    input_variables=["context", "question"], template=prompt_template_str
)
