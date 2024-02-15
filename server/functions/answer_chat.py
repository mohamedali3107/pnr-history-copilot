def answer(question, qa_chain):
    """
    Return the answer of an LLM to a query via a langchain ConversationalRetrievalChain.
    Used for chatbot.

    Parameters:
    - question (str): the question/query of the user
    - qa_chain (langchain ConversationalRetrievalChain): the chain that calls the LLM

    Return:
    str: the answer of the LLM
    """
    if not qa_chain:
        return "Unknown"

    return qa_chain({"question": question})["answer"]


def answer_retrieval_chain(question, qa_chain):
    """
    Return the answer of an LLM to a query via a Langchain RetrievalQA chain.
    Used for computing key points paragraphs and fill templates.

    Parameters:
    - question (str): the question/query of the user
    - qa_chain (langchain type RetrievalQA): the chain that calls the LLM

    Return:
    str: the answer of the LLM
    """
    if not qa_chain:
        return "Unknown"

    return qa_chain({"query": question})["result"]
