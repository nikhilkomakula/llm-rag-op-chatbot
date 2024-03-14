i

# OpenPages IntelliBot

Welcome to OpenPages IntelliBot, your intelligent and efficient chatbot powered by the state-of-the-art Retrieval-Augmented Generation (RAG) technique and Large Language Model (LLM).

## What is OpenPagesIntelliBot?

OpenPagesIntelliBot leverages cutting-edge AI technologies to provide you with instant and accurate responses about OpenPages, its features, solutions / modules it offers and its trigger framework. By combining the power of RAG and Zephyr LLM, OpenPagesIntelliBot ensures that you receive contextually relevant information.

## How RAG Works?

![RAG Diagram](images/RAG_workflow.png)

[Image Credit](https://huggingface.co/learn/cookbook/en/rag_evaluation)

#### Step 1: Data Collection

Gather all the data that is needed for your application. In the case of OpenPages IntelliBot, this include administrators guide, solutions or modules offerings, users guide and trigger developer guide.

#### Step 2: Data Chunking

Data chunking is the process of breaking your data down into smaller, more manageable pieces. For instance, if you have a lengthy 100-page user manual, you might break it down into different sections, each potentially answering different customer questions.

This way, each chunk of data is focused on a specific topic. When a piece of information is retrieved from the source dataset, it is more likely to be directly applicable to the user’s query, since we avoid including irrelevant information from entire documents.

This also improves efficiency, since the system can quickly obtain the most relevant pieces of information instead of processing entire documents.

#### Step 3: Document Embeddings

Now that the source data has been broken down into smaller parts, it needs to be converted into a vector representation. This involves transforming text data into embeddings, which are numeric representations that capture the semantic meaning behind text.

In simple words, document embeddings allow the system to understand user queries and match them with relevant information in the source dataset based on the meaning of the text, instead of a simple word-to-word comparison. This method ensures that the responses are relevant and aligned with the user’s query.

#### Step 4: Data Retrieval

When a user query enters the system, it must also be converted into an embedding or vector representation. The same model must be used for both the document and query embedding to ensure uniformity between the two.

Once the query is converted into an embedding, the system compares the query embedding with the document embeddings. It identifies and retrieves chunks whose embeddings are most similar to the query embedding, using measures such as cosine similarity.

These chunks are considered to be the most relevant to the user’s query.

#### Step 5: Response Generation

The retrieved text chunks, along with the initial user query, are fed into a language model. The algorithm will use this information to generate a coherent response to the user’s questions through a chat interface.

## Sources used for OpenPages IntelliBot:

OpenPages IntelliBot can answer questions related to:

- OpenPages Administration
- OpenPages Solutions or Modules
- OpenPages Trigger Development

## How to Use OpenPages IntelliBot?

1. Simply type your query or question into the chat interface.
2. OpenPages IntelliBot will process your query using the RAG model and provide you with a contextually relevant response.

## Get Started to Run Locally:

**Step 1:** Download the Git repository

**Step 2:** Install dependencies

```python
python install -r requirements.txt
```

**Step 3:** Rename `dotenv` file to `.env` and set `HUGGINGFACEHUB_API_TOKEN` with your API token.

**Step 4:** Run the application

```python
python app.py
```

## Build and Run Container Locally:

**Step 1:** Build image (replace `<docker_id>` with your Docker ID)

```python
docker build --tag <docker_id>/llm-rag-op-chatbot .
```

**Step 2:** Run container (replace `<docker_id>` with your Docker ID and `api_token` with your Hugging Face API Token)

```python
docker run -it -d --name llm-rag-op-chatbot -p 5555:5555 -e HUGGINGFACEHUB_API_TOKEN=<api_token> <docker_id>/llm-rag-op-chatbot:latest
```

**Note 1:** List all containers

```python
docker ps -a
```

**Note 2:** Review the logs

```python
docker logs -f llm-rag-op-chatbot
```

## Technologies Used:

* **PDF Parser :** PyMuPDFLoader
* **Vector Database :** ChromaDB
* **Orchestration Framework :** LangChain
* **Embedding Model :** BAAI/bge-large-en-v1.5
* **Large Language Model :** huggingfaceh4/zephyr-7b-beta

## Contact Me:

For any inquiries or feedback, please contact me at [nikhil.komakula@outlook.com](mailto:nikhil.komakula@outlook.com).

## License:	

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) - see the [LICENSE](LICENSE) file for details.

---

**Note:** OpenPages IntelliBot is for demonstration purposes only and may not provide accurate information in all scenarios. Always verify critical information from reliable sources.
