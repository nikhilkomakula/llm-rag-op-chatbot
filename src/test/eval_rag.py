# import libraries
import os
import time
import datetime
import pandas as pd

# import functions
from src.test.eval_custom_model import LLM, eval_rag_metrics
from src.retrieval.retriever_chain import load_hf_llm

# constants
EVAL_LLM = "mistralai/Mistral-7B-v0.1" # "mistralai/Mistral-7B-Instruct-v0.2"
EVAL_LLM_NAME = "Mistral 7B"
EVAL_FILE_PATH = "./src/test/eval_questions.txt"
EVAL_RESULTS_FILE_NAME = "eval_results_{0}.csv"
EVAL_RESULTS_PATH = "./src/test"


# format context documents as list
def format_docs_as_list(docs):
    """
    Converts context documents as list
    
    Args:
        docs (list): List of Document objects

    Returns:
        list: Returns list of documents.
    """
    return [doc.page_content for doc in docs]

# load eval questions
def load_eval_questions():
    """
    Loads eval questions into memory.

    Returns:
        list: Returns list of questions.
    """

    eval_questions = []
    with open(EVAL_FILE_PATH, "r") as file:
        for line in file:
            # Remove newline character and convert to integer
            item = line.strip()
            eval_questions.append(item)

    return eval_questions


# evaluate rag chain
def evaluate_rag(chain_name, rag_chain):
    """
    Evaluates the rag pipeline based on eval questions.

    Args:
        chain_name (str): QA Chain name.
        rag_chain (Runnable): QA Chain instance.
    """

    columns = ["Chain", "Question", "Response", "Time"]
    df = pd.DataFrame(columns=columns)

    # load evaluation questions
    eval_questions = load_eval_questions()
    
    # instantiate hf llm
    hf_eval_llm = load_hf_llm(repo_id=EVAL_LLM, max_new_tokens=512, temperature=0.4)

    # instantiate deepeval llm
    eval_custom_model = LLM(model_name=EVAL_LLM_NAME, model=hf_eval_llm)

    for question in eval_questions:

        start_time = time.time()
        response = rag_chain.invoke(question)
        print("Response", response)
        end_time = time.time()
        
        query = response['query']
        answer = response['result']
        context = format_docs_as_list(response['context'])
        metrics = eval_rag_metrics(eval_custom_model, question, answer, context)

        row = {
            "Chain": chain_name,
            "Question": query,
            "Response": answer,
            "Time": "{:.2f}".format(round(end_time - start_time, 2)),
            "Metrics": metrics
        }
        
        print("*" * 100)
        print("Question:", question)
        print("Answer:", answer)
        print("Response Time:", "{:.2f}".format(round(end_time - start_time, 2)))
        print("Metrics:", metrics)
        print("*" * 100)

        df = pd.concat([df, pd.DataFrame.from_records([row])])

    CSV = EVAL_RESULTS_FILE_NAME.format(
        datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    )
    print(os.path.join(EVAL_RESULTS_PATH, CSV))
    df.to_csv(os.path.join(EVAL_RESULTS_PATH, CSV), index=False)
