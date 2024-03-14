# import libraries
import os
from langchain_community.document_loaders import PyMuPDFLoader

# constants
DATA_DIR = "../../data/"


# load data
def load_documents():
    """
    Loads documents into memory.

    Raises:
        e: Any exception while loading the documents.

    Returns:
        list: An array of documents.
    """

    documents = []
    try:
        for root, _, files in os.walk(DATA_DIR):
            for file in files:
                if file.endswith(".pdf"):
                    print(f"Reading File: {file}")

                    # read PDF
                    loader = PyMuPDFLoader(os.path.join(root, file))
                    document = loader.load()

                    # append to docs
                    documents += document
    except Exception as e:
        print("Error while loading the data!", e)
        raise e
    return documents
