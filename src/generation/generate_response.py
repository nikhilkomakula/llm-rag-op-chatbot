# import libraries
import time
from typing import Optional

# import functions
from src.retrieval.retriever_chain import get_base_retriever, load_hf_llm, create_qa_chain, create_qa_chain_eval

# constants
HF_MODEL        = "huggingfaceh4/zephyr-7b-alpha"  # "mistralai/Mistral-7B-Instruct-v0.2" # "google/gemma-7b"
EMBEDDING_MODEL = "BAAI/bge-large-en-v1.5"


# get the qa chain
def get_qa_chain():
    """
    Instantiates QA Chain.

    Returns:
        Runnable: Returns an instance of QA Chain.
    """

    # get retriever
    retriever = get_base_retriever(embedding_model=EMBEDDING_MODEL, k=4, search_type="mmr")

    # instantiate llm
    llm = load_hf_llm(repo_id=HF_MODEL, max_new_tokens=512, temperature=0.4)

    # instantiate qa chain
    qa_chain = create_qa_chain(retriever, llm)

    return qa_chain

# function to get the global qa chain
def set_global_qa_chain(local_qa_chain):
    """
    Sets the Global QA Chain.

    Args:
        local_qa_chain: Local QA Chain.
    """
    global global_qa_chain
    global_qa_chain = local_qa_chain

# function to invoke the rag chain
def invoke_chain(query: str):
    """
    Invokes the chain to generate the response.

    Args:
        query (str): Question asked by the user.

    Returns:
        str: Returns the generated response.
    """
    max_attempts = 3  # Maximum number of retry attempts

    for attempt in range(max_attempts):
        try:
            response = global_qa_chain.invoke(query)
            return response  # If successful, return the response
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error:", e)
    else:
        return "All attempts failed. Unable to get response."

    
# function to generate streamlit response
def generate_response(query: str):
    """
    Generates response based on the question being asked.

    Args:
        query (str): Question asked by the user.
        history (dict): Chat history. NOT USED FOR NOW.

    Returns:
        str: Returns the generated response.
    """

    # invoke chain
    print("*" * 100)
    print("Question:", query)
    start_time = time.time()
    try:
        response = global_qa_chain.invoke(query)
    except Exception as e:
        print("Error:", e)
        response = global_qa_chain.invoke(query)
    print("Answer:", response)
    end_time = time.time()
    print("Response Time:", "{:.2f}".format(round(end_time - start_time, 2)))
    print("*" * 100)
    return response

# function to generate streamlit response
def generate_response_streamlit(message: str, history: Optional[dict]):
    """
    Generates response based on the question being asked.

    Args:
        message (str): Question asked by the user.
        history (dict): Chat history. NOT USED FOR NOW.

    Returns:
        str: Returns the generated response.
    """

    response = generate_response(message)
    response = response.replace("\n", "  \n")
    for word in response.split(" "):
        yield word + " "
        time.sleep(0.05)
        
# function to generate response
def generate_response_gradio(message: str, history: Optional[dict]):
    """
    Generates response based on the question being asked.

    Args:
        message (str): Question asked by the user.
        history (dict): Chat history. NOT USED FOR NOW.

    Returns:
        str: Returns the generated response.
    """

    response = generate_response(message)
    for i in range(len(response)):
        time.sleep(0.01)
        yield response[: i+1]

# function to check if the global variable has been set
def has_global_variable():
    """
    Checks if global_qa_chain has been set.

    Returns:
        bool: Returns True if set. Otherwise False.
    """
    if 'global_qa_chain' in globals():
        return True
    
    return False

# get the qa chain for evaluation
def get_qa_chain_eval():
    """
    Instantiates QA Chain for evaluation.

    Returns:
        Runnable: Returns an instance of QA Chain.
    """

    # get retriever
    retriever = get_base_retriever(embedding_model=EMBEDDING_MODEL, k=4, search_type="mmr")

    # instantiate llm
    llm = load_hf_llm(repo_id=HF_MODEL, max_new_tokens=512, temperature=0.4)

    # instantiate qa chain
    qa_chain = create_qa_chain_eval(retriever, llm)

    return qa_chain