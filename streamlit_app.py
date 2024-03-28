# import libraries
import os
import streamlit as st
from dotenv import find_dotenv, load_dotenv

# import functions
from src.ui.streamlit_chat_interface import create_streamlit_chatinterface
from src.generation.generate_response import get_qa_chain, set_global_qa_chain, generate_response_streamlit, has_global_variable

def main():

    # find .env automatically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())
    
    if "HUGGINGFACEHUB_API_TOKEN" not in os.environ:
        os.environ["HUGGINGFACEHUB_API_TOKEN"] = st.secrets["HUGGINGFACEHUB_API_TOKEN"]
        
    if not has_global_variable():

        # get the qa chain
        qa_chain = get_qa_chain()

        # set the global qa chain
        set_global_qa_chain(qa_chain)
    
    # initiate the chat interface
    create_streamlit_chatinterface(generate_response_streamlit)

if __name__ == "__main__":
    main()