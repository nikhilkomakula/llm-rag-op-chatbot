# import libraries
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import HuggingFaceEndpoint
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# import functions
from ..indexing.build_indexes import retrieve_indexes


# instantiate base retriever
def get_base_retriever(k=4, search_type="mmr"):
    """
    Instantiates base retriever.

    Args:
        k (int, optional): Top k results to retrieve. Defaults to 4.
        search_type (str, optional): Search type (mmr or similarity). Defaults to 'mmr'.

    Returns:
        VectorStoreRetriever: Returns base retriever.
    """

    # get the vector store of indexes
    vector_store = retrieve_indexes()

    base_retriever = vector_store.as_retriever(
        search_type=search_type, search_kwargs={"k": k}
    )

    return base_retriever


# define prompt template
def create_prompt_template():
    """
    Creates prompt template.

    Returns:
        PromptTemplate: Returns prompt template.
    """
    prompt_template = """
        <|system|>
        You are an AI assistant for question-answering tasks. Use the provided context to answer the question. If you don't know the answer, just say that you don't know. The generated answer should be relevant to the question being asked, short and concise. Do not be creative and do not make up the answer.</s>
        {context}</s>
        <|user|>
        {query}</s>
        <|assistant|>
    """
    chat_prompt_template = ChatPromptTemplate.from_template(prompt_template)
    return chat_prompt_template


# define llm
def load_hf_llm(repo_id, max_new_tokens=512, temperature=0.2):
    """
    Loads Hugging Face Endpoint for inference.

    Args:
        repo_id (str): HuggingFace Model Repo ID.
        max_new_tokens (int, optional): Maximum number of new tokens to generate. Defaults to 512.
        temperature (float, optional): Temperature setting. Defaults to 0.2.

    Returns:
        HuggingFaceEndpoint: Returns HuggingFace Endpoint.
    """

    hf_llm = HuggingFaceEndpoint(
        repo_id=repo_id,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        do_sample=True,
        repetition_penalty=1.1,
        return_full_text=False,
    )
    return hf_llm


# define retrieval chain
def create_qa_chain(retriever, llm):
    """
    Instantiates qa chain.

    Args:
        retriever (VectorStoreRetriever): Vector store.
        llm (HuggingFaceEndpoint): HuggingFace endpoint.

    Returns:
        Runnable: Returns qa chain.
    """

    qa_chain = (
        {"context": retriever, "query": RunnablePassthrough()}
        | create_prompt_template()
        | llm
        | StrOutputParser()
    )
    return qa_chain
