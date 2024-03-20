# import libraries
import os
from typing import List, Optional
from transformers import AutoTokenizer
from langchain_community.vectorstores import Chroma
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.docstore.document import Document

# import functions
from ..data.load_dataset import load_documents

# constants
INDEX_DIR = "indexes/"
EMBEDDING_MODEL = "BAAI/bge-large-en-v1.5"


# instantiate embedding model
def load_embedding_model():
    """
    Load the embedding model.

    Returns:
        HuggingFaceBgeEmbeddings: Returns the embedding model.
    """

    # check if GPU is available
    import tensorflow as tf

    device = "cuda" if tf.test.gpu_device_name() else "cpu"
    print("device:", device)

    hf_bge_embeddings = HuggingFaceBgeEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": device},
        encode_kwargs={
            "normalize_embeddings": True # set True to compute cosine similarity
        }
    )

    # To get the value of the max sequence_length, we will query the underlying `SentenceTransformer` object used in the RecursiveCharacterTextSplitter.
    print(
        f"Model's maximum sequence length: {SentenceTransformer(EMBEDDING_MODEL).max_seq_length}"
    )

    return hf_bge_embeddings


# split documents
def chunk_documents(
    chunk_size: int,
    knowledge_base: List[Document],
    tokenizer_name: Optional[str] = EMBEDDING_MODEL,
) -> List[Document]:
    """
    Split documents into chunks of maximum size `chunk_size` tokens and return a list of documents.

    Args:
        chunk_size (int): Chunk size.
        knowledge_base (List[Document]): Loaded documents.
        tokenizer_name (Optional[str], optional): Embedding Model name. Defaults to EMBEDDING_MODEL.

    Returns:
        List[Document]: Returns chunked documents.
    """

    text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
        AutoTokenizer.from_pretrained(tokenizer_name),
        chunk_size=chunk_size,
        chunk_overlap=int(chunk_size / 10),
        add_start_index=True,
        strip_whitespace=True,
        separators=["\n\n", "\n", ".", ""],
    )

    docs_processed = []
    for doc in knowledge_base:
        docs_processed += text_splitter.split_documents([doc])

    # Remove duplicates
    unique_texts = {}
    docs_processed_unique = []
    for doc in docs_processed:
        if doc.page_content not in unique_texts:
            unique_texts[doc.page_content] = True
            docs_processed_unique.append(doc)

    return docs_processed_unique


# generate indexes
def generate_indexes():
    """
    Generates indexes.

    Returns:
        ChromaCollection: Returns vector store.
    """

    # load documents
    documents = load_documents()

    # chunk documents to honor the context length
    chunked_documents = chunk_documents(
        SentenceTransformer(
            EMBEDDING_MODEL
        ).max_seq_length,  # We choose a chunk size adapted to our model
        documents,
        tokenizer_name=EMBEDDING_MODEL,
    )

    # save indexes to disk
    vector_store = Chroma.from_documents(
        documents=chunked_documents,
        embedding=load_embedding_model(),
        collection_metadata={"hnsw:space": "cosine"},
        persist_directory=INDEX_DIR,
    )

    return vector_store


# load indexes from disk
def load_indexes():
    """
    Loads indexes into memory.

    Returns:
        ChromaCollection: Returns vector store.
    """

    vector_store = Chroma(
        persist_directory=INDEX_DIR, embedding_function=load_embedding_model()
    )
    return vector_store


# retrieve vector store
def retrieve_indexes():
    """
    Retrieves indexes.

    Returns:
        ChromaCollection: Returns vector store.
    """

    if [f for f in os.listdir(INDEX_DIR) if not f.startswith(".")] == []:
        print("Generating indexes...")
        return generate_indexes()
    else:
        print("Loading existing indexes!")
        return load_indexes()
