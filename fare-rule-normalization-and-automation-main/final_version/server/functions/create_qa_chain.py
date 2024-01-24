from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.chains import ConversationalRetrievalChain, RetrievalQA

_ = load_dotenv(find_dotenv())  # read local .env file

deployment_name = "gpt-4-0613"
embedding_name = "text-embedding-ada-002"
llm = AzureChatOpenAI(deployment_name=deployment_name, streaming=True, temperature=0)


def create_qa_chain(vector_store, chat_history, prompt, llm=llm):
    """Return a Q&A chain with memory.

    Parameters:
    - vector_store (VectorStore): a Langchain vectorstore
    - chat_history (list): the history to be taken into account by the chain
    - prompt (PromptTemplate instance): the prompt template to be used
    - Optional llm (LLM model, e.g. AzureChatOpenAI instance): the language model to be used

    Return:
    ConversationalRetrievalChain instance: a Q&A chain
    """
    retriever = vector_store.as_retriever(
        search_type="similarity", search_kwargs={"k": 5}
    )

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=chat_history,
        get_chat_history=lambda h: h,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": prompt},
    )

    return qa_chain


def chain_paragraph(
    vector_store, prompt, llm=llm, nb_chunks=11, search_type="similarity"
):
    """Return a Q&A chain.

    Parameters:
    - vector_store (VectorStore): a Langchain vectorstore
    - prompt (PromptTemplate instance): the prompt template to be used
    - Optional llm (LLM model, e.g. AzureChatOpenAI instance): the language model to be used
    - Optional nb_chunks (int): the number of chunks to retrieve for each query
    - Optional search_type (str): the search type to be performed at retrieval stage in the vectorstore

    Return:
    ConversationalRetrievalChain instance: a Q&A chain
    """
    retriever = vector_store.as_retriever(
        search_type=search_type, search_kwargs={"k": nb_chunks}
    )

    chain = RetrievalQA.from_chain_type(
        llm, retriever=retriever, chain_type_kwargs={"prompt": prompt}
    )

    return chain
