# 📄 RAG Document Q&A Chatbot

### 🚀 Overview
An AI-powered chatbot that allows users to upload PDF documents and ask questions about them using **Retrieval-Augmented Generation (RAG)**. The system retrieves relevant document chunks and generates accurate, context-aware answers.

---

## ✨ Features

- 📂 Upload any PDF directly from the browser  
- 💬 Ask questions in natural language  
- 📍 Get answers with exact source page references  
- 🧠 Context-aware responses using RAG (reduces hallucination)  
- 🗂️ Persistent chat history stored in SQLite  
- 🎯 Clean, ChatGPT-like user interface  

---

## 🧠 How It Works (RAG Pipeline)

1. **PDF Processing**
   - Document is split into chunks of ~1000 characters  
   - Overlap of 200 characters ensures context continuity  

2. **Embedding Generation**
   - Each chunk is converted into vector embeddings using Gemini  

3. **Vector Storage**
   - Embeddings are stored locally in **ChromaDB**  

4. **Query Handling**
   - User query is converted into an embedding  
   - Top 3 most relevant chunks are retrieved  

5. **Answer Generation**
   - Retrieved chunks are passed as context to Gemini  
   - Model generates answers strictly based on this context  

---

## 🛠️ Tech Stack

| Layer        | Technology                     |
|--------------|-------------------------------|
| LLM          | Google Gemini 2.5 Flash       |
| Embeddings   | Gemini Embedding 001          |
| Vector DB    | ChromaDB                      |
| Backend      | FastAPI                       |
| Frontend     | Streamlit                     |
| Database     | SQLite                        |
| Language     | Python 3.12                   |

---

## 🔌 API Endpoints

| Method | Endpoint   | Description                                      |
|--------|------------|--------------------------------------------------|
| GET    | `/`        | Health check                                     |
| POST   | `/upload`  | Upload and process a PDF                         |
| POST   | `/ask`     | Ask a question and receive answer + sources      |
| GET    | `/history` | Retrieve last 20 Q&A interactions                |

---

## 📁 Project Structure
rag-chatbot/
├── main.py # FastAPI backend
├── app.py # Streamlit frontend
├── ingest.py # PDF ingestion script
├── ask.py # Question answering script
├── database.py # SQLite chat history
├── data/ # Uploaded PDFs
└── chroma_db/ # Vector embeddings storage


---

## ⚙️ Setup Instructions

### 1. Clone the Repository


git clone https://github.com/VijayKakde/rag-chatbot.git
cd rag-chatbot
2. Create Virtual Environment
python -m venv venv
venv\Scripts\activate
3. Install Dependencies
pip install fastapi uvicorn streamlit requests langchain
pip install langchain-community langchain-text-splitters
pip install chromadb pypdf python-dotenv google-genai
4. Configure Environment Variables

Create a .env file in the root directory:

GEMINI_API_KEY=your_api_key_here
5. Run Backend (FastAPI)
uvicorn main:app --reload
6. Run Frontend (Streamlit)
streamlit run app.py
🧪 Example Workflow
Open the Streamlit app
Upload a PDF document
Ask questions like:
"What is the main topic of this document?"
"Summarize page 5"
Get accurate answers with source references
🎯 Key Advantages
✅ Reduces hallucination using RAG
⚡ Fast retrieval with ChromaDB
🔒 Fully local vector storage
📊 Traceable answers with sources
🧩 Modular architecture (easy to extend)
🚧 Future Improvements
Multi-document querying
Support for DOCX / TXT files
Authentication system
Deployment (Docker / Cloud)
Streaming responses
👨‍💻 Author

Vijay Kakde
AI & Data Science Engineer


If you paste this into `README.md`, it will render perfectly on GitHub.

If you want next level:
- I can add **badges (stars, forks, Python, license)**  
- Or make a **portfolio-ready version for placements (very impactful)**
