# import libraries
from dotenv import find_dotenv, load_dotenv

# import functions
from src.ui.gradio_chat_interface import create_gradio_chatinterface
from src.generation.generate_response import get_qa_chain, set_global_qa_chain, generate_response_gradio

def main():

    # find .env automatically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    # get the qa chain
    qa_chain = get_qa_chain()

    # set the global qa chain
    set_global_qa_chain(qa_chain)
    
    # initiate the chat interface
    create_gradio_chatinterface(generate_response_gradio).launch(server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    main()