# import libraries
import sys
from dotenv import find_dotenv, load_dotenv

# import functions
from src.test.eval_rag import evaluate_rag
from src.ui.chat_interface import create_chatinterface
from src.generation.generate_response import get_qa_chain, set_global_qa_chain, generate_response

# find .env automatically by walking up directories until it's found, then
# load up the .env entries as environment variables
load_dotenv(find_dotenv())

if __name__ == "__main__":

    # get the qa chain
    qa_chain = get_qa_chain()

    if len(sys.argv) > 1:
        evaluate_rag("qa_chain", qa_chain)
    else:
        set_global_qa_chain(qa_chain)
        create_chatinterface(generate_response).launch(server_name="0.0.0.0", server_port=5555)
