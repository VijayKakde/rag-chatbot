Project Title
RAG Document Q&A Chatbot
One liner
An AI-powered chatbot that lets you upload any PDF and ask questions about it — built with Retrieval-Augmented Generation (RAG).

What it does

Upload any PDF document through the browser
Asks questions in natural language and gets accurate answers
Shows exactly which page of the document the answer came from
Stores full chat history in a local database
Clean chat UI just like ChatGPT


Tech Stack
LayerTechnologyLLMGoogle Gemini 2.5 FlashEmbeddingsGemini Embedding 001Vector DBChromaDBBackendFastAPIFrontendStreamlitDatabaseSQLiteLanguagePython 3.12

How RAG works in this project

PDF is loaded and split into 1000-character chunks with 200-character overlap
Each chunk is converted to a vector embedding using Gemini
Embeddings are stored in ChromaDB locally
When user asks a question, the question is also embedded
ChromaDB finds the 3 most similar chunks to the question
Those chunks are sent to Gemini as context
Gemini answers using only that context — no hallucination


API Endpoints
MethodEndpointDescriptionGET/Health checkPOST/uploadUpload and ingest a PDFPOST/askAsk a question, get answer + sourcesGET/historyGet last 20 Q&A pairs from SQLite

Project Structure
rag-chatbot/
├── main.py          # FastAPI backend
├── app.py           # Streamlit frontend
├── ingest.py        # Standalone PDF ingestion script
├── ask.py           # Standalone question answering script
├── database.py      # SQLite chat history
├── data/            # PDF storage
└── chroma_db/       # Vector embeddings storage

Setup Instructions
bash# 1. Clone the repo
git clone https://github.com/VijayKakde/rag-chatbot.git
cd rag-chatbot

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install fastapi uvicorn streamlit requests langchain
pip install langchain-community langchain-text-splitters
pip install chromadb pypdf python-dotenv google-genai

# 4. Add your Gemini API key
# Create a .env file and add:
# GEMINI_API_KEY=your_key_here

# 5. Run FastAPI backend
uvicorn main:app --reload

# 6. Run Streamlit frontend (new terminal)
streamlit run app.py
