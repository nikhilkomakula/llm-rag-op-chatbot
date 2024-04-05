---
title: OpenPages IntelliBot
emoji: 🤖
colorFrom: yellow
colorTo: pink
sdk: docker
app_port: 7860
pinned: true
license: mit
---
[![Sync to Hugging Face hub](https://github.com/nikhilkomakula/llm-rag-op-chatbot/actions/workflows/main.yml/badge.svg)](https://github.com/nikhilkomakula/llm-rag-op-chatbot/actions/workflows/main.yml)

# OpenPages IntelliBot

Welcome to OpenPages IntelliBot, your intelligent and efficient chatbot powered by the state-of-the-art Retrieval-Augmented Generation (RAG) technique and Large Language Model (LLM).

****Streamlit:** [![Try it!](https://img.shields.io/badge/Try_it!-blue.svg)](https://nk-openpages-intellibot.streamlit.app)**

**Gradio:** [![Try it!](https://img.shields.io/badge/Try_it!-blue.svg)](https://huggingface.co/spaces/nikhilkomakula/llm-rag-op-chatbot)

## What is OpenPages IntelliBot?

OpenPagesIntelliBot leverages cutting-edge AI technologies to provide you with instant and accurate responses about OpenPages, its features, solutions / modules it offers and its trigger framework. By combining the power of RAG and Zephyr LLM, OpenPagesIntelliBot ensures that you receive contextually relevant information.

## How Retrieval-Augmented Generation (RAG) Works?

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

* Gradio

```python
python app.py -gradio
```

    OR

```python
python gradio_app.py
```

* Streamlit

```python
python app.py -streamlit
```

    OR

```python
streamlit run streamlit_app.py
```

## Build and Run Container Locally:

**Step 1:** Build image (replace `<docker_id>` with your Docker ID)

```python
docker build --tag <docker_id>/llm-rag-op-chatbot .
```

**Step 2:** Run container (replace `<docker_id>` with your Docker ID)

```python
docker run -it -d --name llm-rag-op-chatbot -p 7860:7860 -e HUGGINGFACEHUB_API_TOKEN=<api_token> <docker_id>/llm-rag-op-chatbot:latest
```

**Note 1:** List all containers

```python
docker ps -a
```

**Note 2:** Review the logs

```python
docker logs -f llm-rag-op-chatbot
```

## RAG Evaluation:

Used [DeepEval](https://github.com/confident-ai/deepeval) open-source LLM evaluation framework for evaluating the performance of the RAG pipeline. Below metrics are used to evaluate its performance:

* **Answer Relevancy:** Measures the quality of your RAG pipeline's generator by evaluating how relevant the `actual_output` of your LLM application is compared to the provided `input`.
* **Faithfulness:** Measures the quality of your RAG pipeline's generator by evaluating whether the `actual_output` factually aligns with the contents of your `retrieval_context`.
* **Contextual Relevancy:** Measures the quality of your RAG pipeline's retriever by evaluating the overall relevance of the information presented in your `retrieval_context` for a given `input`.
* **Hallucination:** Determines whether your LLM generates factually correct information by comparing the `actual_output` to the provided `context`.
* **Bias:** Determines whether your LLM output contains gender, racial, or political bias.
* **Toxicity:** Evaluates toxicness in your LLM outputs.

## REST API (Gradio Only):

**Note:** Navigate to the chat interface UI in the browser and locate `Use via API` and click on it. A fly over opens on the right hand side. Capture the URL under the title named `API documentation`.

* **URL:** `<http|https>`://`<hostname`:`<port>`/run/chat
* **METHOD:** POST
* **BODY:** { "data": ["`<query>`", ""] }

## Technologies Used:

* **PDF Parser :** PyMuPDFLoader
* **Vector Database :** ChromaDB
* **Orchestration Framework :** LangChain
* **Embedding Model :** BAAI/bge-large-en-v1.5
* **Large Language Model :** huggingfaceh4/zephyr-7b-alpha
* **UI Framework** : Streamlit & Gradio

## CI/CD:

* **Streamlit.io**
  * Committing any changes to the git branch `deploy-to-streamlit` will deploy to streamlit.io.
* **Hugging Face Spaces**
  * Committing any changes to the git branch `deploy-to-hf-spaces` will deploy to Hugging Face Spaces as a Docker space.

## Streamlit.io Deployment:

If you are encountering issues with `sqlite` version, then run the following steps:

* Add the following dependency to `requirements.txt`:

  `pysqlite3-binary==0.5.2.post3`
* Add the following block of code to `streamlit_app.py` at the beginning of the file:

```
# code to fix the issue with sqllite version on streamlit.io
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
```

**Note:** If running locally for Streamlit UI interace and if you hit any errors with `pysqlite3`, try removing whatever that is mentioned above.

## Enhancements:

* Different advanced retrieval methods could be used.
* Context re-ranking can be implemented.
* Latest LLMs could be used for better performance.
* Could be converted to `conversational` AI chatbot.
* Utilize better PDF parsers and experiment with `chunk_size` and `chunk_overlap` properties.
* Fine-tuning the LLM on the proprietary dataset might improve the results.

## Contact Me:

For any inquiries or feedback, please contact me at [nikhil.komakula@outlook.com](mailto:nikhil.komakula@outlook.com).

## License:

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) - see the [LICENSE](LICENSE) file for details.

---

**Note:** OpenPages IntelliBot is for demonstration purposes only and may not provide accurate information in all scenarios. Always verify critical information from reliable sources.
