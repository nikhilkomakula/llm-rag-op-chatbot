# import libraries
import gradio as gr

# import functions
from src.test.eval_rag import load_eval_questions


# create chatbot interface
def create_gradio_chatinterface(generate_response):
    """
    Instantiates the gradio chat interface.

    Args:
        generate_response (callable): Function that generates the response.

    Returns:
        class: Returns gradio chatinterface class
    """

    chat_interface = gr.ChatInterface(
        fn=generate_response,
        textbox=gr.Textbox(
            placeholder="Type your question here!", container=False, scale=7
        ),
        title="OpenPages IntelliBot",
        description="Ask me about OpenPages (v9.0), its features, solutions / modules it offers and the trigger framework. Authored by Nikhil Komakula (nikhil.komakula@outlook.com).",
        theme=gr.themes.Default(primary_hue="blue"),
        examples=load_eval_questions(),
        cache_examples=False,
        concurrency_limit=None
    )

    return chat_interface
