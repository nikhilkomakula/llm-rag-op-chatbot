# import libraries
from dotenv import find_dotenv, load_dotenv

# import functions
from src.test.eval_rag import evaluate_rag
from src.generation.generate_response import get_qa_chain

def main():

    # find .env automatically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    # get the qa chain
    qa_chain = get_qa_chain()
    
    # evaluate the qa chain
    evaluate_rag("qa_chain", qa_chain)

if __name__ == "__main__":
    main()