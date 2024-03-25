# import libraries
import streamlit as st

# import functions
from src.test.eval_rag import load_eval_questions
        
# initialize streamlit
def create_streamlit_chatinterface(generate_response):
    """
    Instantiates the streamlit chat interface.

    Args:
        generate_response (callable): Function that generates the response.
    """

    st.title("OpenPages IntelliBot")
    st.caption("Ask me about OpenPages (v9.0), its features, solutions / modules it offers and the trigger framework. Authored by Nikhil Komakula (nikhil.komakula@outlook.com).")
    st.divider()    

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Type your question here!"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner(""):
                response = st.write_stream(generate_response(prompt, st.session_state.messages))
                
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

    # option = st.selectbox("Examples:", tuple(load_eval_questions()))
    # if option:
    #     st.chat_message(option)