# RBI NBFC Chatbot

The **RBI NBFC Chatbot** is designed to help users query complex RBI notifications and NBFC rules efficiently.  
It leverages **document retrieval (FAISS)** to ground responses in official RBI PDFs and uses **Google Gemini LLM** to generate detailed, human-like answers.

---

## Key Features

- Search and answer queries based on RBI NBFC documents  
- Retrieval-Augmented Generation (RAG) for grounded answers  
- Maintains conversation history in a sidebar  
- Optional simple LLM QA mode for direct responses  
- Evaluation framework using **LangSmith** and RBI FAQ dataset  

---

## Approach

### 1. Data Preparation
- Load RBI PDF (`rbi.pdf`)  
- Chunk text using `RecursiveCharacterTextSplitter`  
- Generate embeddings using `HuggingFaceEmbeddings`  
- Store embeddings in **FAISS** index  

### 2. Chatbot Development (RAG)
- Load FAISS index and create a retriever  
- Use **Google Gemini API** LLM to answer queries  
- Streamlit interface with conversation history  

### 3. Evaluation
- Use RBI FAQ dataset as ground truth  
- Evaluate chatbot responses using **LangSmith**  

---

## Challenges & Solutions

| Challenge                        | Solution                                                    |
| -------------------------------- | ----------------------------------------------------------- |
| Large RBI PDFs                   | Chunked text for FAISS embeddings                           |
| C drive space issues             | Installed Python, venv, and FAISS on E drive; cleared cache |
| Grounded answers                 | Implemented RAG with FAISS + Gemini LLM                     |
| Maintaining conversation history | Used `st.session_state` in Streamlit                        |
| Evaluation of chatbot            | LangSmith evaluation with RBI FAQ dataset                   |

---

## Retrieval-Augmented Generation (RAG) Pipeline

### Phase 1 – Data Preparation & Indexing
1. Load and clean **RBI Notification PDF**  
2. Split text into chunks  
3. Generate embeddings (`all-MiniLM-L6-v2`)  
4. Store in **FAISS vector database**  

### Phase 2 – Chatbot Development
1. Use **Google Gemini LLM** as reasoning engine  
2. Create retriever from FAISS  
3. Build Retrieval QA Chain with custom prompts  

### Phase 3 – Evaluation with LangSmith
1. Ground truth from **RBI FAQs**  
2. Define evaluation dataset (`faq_dataset.json`)  
3. Run **automatic evaluation**:
   - Strict match  
   - Semantic similarity (QA evaluator)  
4. Analyze results and iterate  

### Phase 4 – Frontend
- Simple **Streamlit UI** for interactive demo  

---

## Requirements

- Python 3.10+  
- Streamlit  
- LangChain  
- FAISS (`faiss-cpu`)  
- HuggingFace Transformers  
- Google Gemini API access  
- LangSmith API  

**Main dependencies**:
   langchain
   langchain-core
   langchain-community
   langchain-google-genai
   langserve
   streamlit
   python-dotenv
   bs4
   pypdf
   faiss-cpu
   sentence-transformers
   huggingface-hub
   google-generativeai
   langsmith
   beautifulsoup4
   requests

- Install all: pip install -r requirements.txt

---

## Usage

1. Unzip the Project
cd project_path

2. Create a virtual environment:

```sh
python -m venv venv  # Create virtual environment
venv\Scripts\activate  # Activate on Windows
```

- If you already have a virtual environment named `.venv`:
```sh
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

2. Install Dependencies
pip install --upgrade pip
pip install -r requirements.txt

3. Set Environment Variables
GOOGLE_API_KEY=your_gemini_api_key_here
LANGSMITH_API_KEY=your_langsmith_api_key_here

4. Data Preparation & Vectorization
jupyter notebook notebooks/data_preparation.ipynb

5. Run the Streamlit app:
streamlit run Home.py

---

## Project Structure

nbfc_qa_chatbot/
├── app/
│   ├── chatbot_chain.py        # RAG Chain logic: FAISS retriever + Gemini LLM → returns a predict() function
│   ├── gemini_chatbot_test.py  # Test script for Gemini API + FAISS integration (development/testing)
│   └── __init__.py             
│
├── data/
│   ├── rbi.pdf                 # RBI Notification PDF (source document for vectorization)
│   └── faiss_index/            # FAISS index (vectorized chunks)
│       ├── index.faiss
│       └── index.pkl
│
├── evaluation/
│   ├── faq_dataset.json        # Ground truth Q&A dataset (RBI FAQs) for evaluation
│   ├── langsmith_eval.py       # Evaluation script using LangSmith for model performance
│   └── scrape_faq.py           # Optional script to scrape RBI FAQ website for additional Q&A
│
├── notebooks/
│   └── data_preparation.ipynb  # Jupyter notebook: PDF ingestion → chunking → embeddings → FAISS index
│
├── pages/                       # Streamlit multipage structure
│   ├── About.py                 # About page (project info, instructions)
│   ├── Chatbot.py               # Main chatbot page (RAG + history)
│   └── History.py               # Page to review chat logs/history
│
├── venv/                        # Python virtual environment (isolated dependencies)
│
├── .env                          # Environment variables (API keys for Gemini & LangChain)
├── Home.py                       # Homepage for Streamlit (redirect to Chatbot page)
├── README.md                     # Project documentation (setup, usage, approach, evaluation)
└── requirements.txt              # Python dependencies (Streamlit, LangChain, FAISS, etc.)

---

## Evaluation

- Dataset: faq_dataset.json (~20 curated Q/A from RBI FAQ page)

- Evaluators:
    1. Strict Match – exact text comparison
    2. Semantic QA Evaluator – checks meaning alignment

- Metrics:
    - Answer accuracy
    - Relevance to context
    - Hallucination detection

- Observations:
    - RAG improved factual grounding
    - Small chunk size + overlap improved retrieval
    - Some answers needed better context window tuning


---

## Future Improvements

- Multi-document ingestion (multiple RBI circulars)
- Hybrid retrieval (keyword + semantic)
- Advanced evaluation (faithfulness, factuality checks)
- Deploy chatbot as HuggingFace Space for public demo


---

## Conclusion

This project demonstrates:
    - End-to-end NLP pipeline: from PDF ingestion → retrieval → QA chain
    - Evaluation-first approach: compare chatbot answers to RBI FAQs with LangSmith
    - Practical deployment: Streamlit frontend for easy demo 
