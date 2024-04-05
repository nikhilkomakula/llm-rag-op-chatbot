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
    
    st.session_state.index = None

    header = st.container()
    header.title("🤖 OpenPages IntelliBot")
    header.caption(
        "Ask me about OpenPages (v9.0), its features, solutions / modules it offers and the trigger framework. Authored by Nikhil Komakula (nikhil.komakula@outlook.com)."
    )
    example_prompt = header.selectbox(
        "Examples:",
        tuple(load_eval_questions()),
        index=st.session_state.index,
        placeholder="Select an example...",
        key='example_prompt'
    )
    header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)

    ### Custom CSS for the sticky header
    st.markdown(
        """
            <style>
                div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
                    position: sticky;
                    top: 2.875rem;
                    background-color: white;
                    z-index: 999;
                }
                .fixed-header {
                    border-bottom: 1px solid rgba(49, 51, 63, 0.6);
                }
                .st-emotion-cache-l9bjmx.e1nzilvr5 p {
                    color: rgba(49, 51, 63, 0.6);
                }
            </style>
        """,
        unsafe_allow_html=True,
    )

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    prompt = st.chat_input("Type your question here!") or example_prompt
    
    if prompt:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner(""):
                response = st.write_stream(
                    generate_response(prompt, st.session_state.messages)
                )

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})