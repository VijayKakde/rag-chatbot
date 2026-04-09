import os
import shutil
import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types
from dotenv import load_dotenv
import chromadb

from database import init_db, save_chat, get_history

load_dotenv()

app = FastAPI(title="RAG Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
CHROMA_DIR = "chroma_db"
DATA_DIR = "data"

init_db()


class QuestionRequest(BaseModel):
    question: str


def get_embedding(text: str, task_type: str = "retrieval_document"):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config=types.EmbedContentConfig(task_type=task_type)
    )
    return response.embeddings[0].values


@app.get("/")
def root():
    return {"message": "RAG Chatbot API is running"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    pdf_path = os.path.join(DATA_DIR, file.filename)
    with open(pdf_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    from langchain_community.document_loaders import PyPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(documents)

    db = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = db.get_or_create_collection("rag_docs")

    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk.page_content)
        collection.add(
            ids=[f"{file.filename}_chunk_{i}"],
            embeddings=[embedding],
            documents=[chunk.page_content],
            metadatas=[chunk.metadata]
        )

    return {
        "message": "PDF uploaded and ingested successfully",
        "filename": file.filename,
        "pages": len(documents),
        "chunks": len(chunks)
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    db = chromadb.PersistentClient(path=CHROMA_DIR)

    try:
        collection = db.get_collection("rag_docs")
    except Exception:
        raise HTTPException(status_code=400, detail="No documents uploaded yet. Please upload a PDF first.")

    query_embedding = get_embedding(request.question, task_type="retrieval_query")

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    context_chunks = results["documents"][0]
    sources = results["metadatas"][0]
    context = "\n\n".join(context_chunks)

    prompt = f"""You are a helpful assistant. Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't find this in the document."

Context:
{context}

Question: {request.question}

Answer:"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    sources_list = [
        {"page": s.get("page", "?"), "preview": c[:150]}
        for s, c in zip(sources, context_chunks)
    ]
    sources_json = json.dumps(sources_list)

    save_chat(request.question, response.text, sources_json)

    return {
        "question": request.question,
        "answer": response.text,
        "sources": sources_list
    }


@app.get("/history")
def chat_history():
    return {"history": get_history()}