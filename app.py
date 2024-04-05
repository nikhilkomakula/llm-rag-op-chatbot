# import libraries
import sys
import subprocess

# Define functions for Gradio and Streamlit interfaces
def run_gradio_interface():
    subprocess.run(["python", "gradio_app.py"])

def run_streamlit_interface():
    subprocess.run(["streamlit", "run", "streamlit_app.py"])
    
def run_rag_evaluate():
    subprocess.run(["python", "eval_app.py"])

# Main function to determine which interface to run
def main():
    if "-gradio" in sys.argv:
        print("Initializing Gradio Interface!")
        run_gradio_interface()
    elif "-streamlit" in sys.argv:
        print("Initializing Streamlit Interface!")
        run_streamlit_interface()
    else:
        print("Running RAG Evaluation!")
        run_rag_evaluate()

# Run the main function
if __name__ == "__main__":
    main()
