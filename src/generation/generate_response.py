# import libraries
from src.retrieval.retriever_chain import get_base_retriever, load_hf_llm, create_qa_chain

# constants
HF_MODEL = "huggingfaceh4/zephyr-7b-beta"  # "mistralai/Mistral-7B-Instruct-v0.2" # "google/gemma-7b"


# get the qa chain
def get_qa_chain():
    """
    Instantiates QA Chain.

    Returns:
        Runnable: Returns an instance of QA Chain.
    """

    # get retriever
    retriever = get_base_retriever(k=4, search_type="mmr")

    # instantiate llm
    llm = load_hf_llm(repo_id=HF_MODEL, max_new_tokens=512, temperature=0.4)

    # instantiate qa chain
    qa_chain = create_qa_chain(retriever, llm)

    return qa_chain


def set_global_qa_chain(local_qa_chain):
    global global_qa_chain
    global_qa_chain = local_qa_chain


# function to generate response
def generate_response(message, history):
    """
    Generates response based on the question being asked.

    Args:
        message (str): Question asked by the user.
        history (dict): Chat history. NOT USED FOR NOW.

    Returns:
        str: Returns the generated response.
    """

    # invoke chain
    response = global_qa_chain.invoke(message)
    print(response)

    return response
