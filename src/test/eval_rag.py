# import libraries
import os
import time
import datetime
import pandas as pd

# constants
EVAL_FILE_PATH = "./src/test/eval_questions.txt"
EVAL_RESULTS_FILE_NAME = "eval_results_{0}.csv"
EVAL_RESULTS_PATH = "./src/test"


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

    eval_questions = load_eval_questions()

    for question in eval_questions:

        start_time = time.time()
        answer = rag_chain.invoke(question)
        end_time = time.time()

        row = {
            "Chain": chain_name,
            "Question": question,
            "Response": answer,
            "Time": "{:.2f}".format(round(end_time - start_time, 2)),
        }

        df = pd.concat([df, pd.DataFrame.from_records([row])])

    CSV = EVAL_RESULTS_FILE_NAME.format(
        datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    )
    print(os.path.join(EVAL_RESULTS_PATH, CSV))
    df.to_csv(os.path.join(EVAL_RESULTS_PATH, CSV), index=False)
