import os
import chromadb
from dotenv import load_dotenv
from google import genai
from google.genai import types
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

PDF_PATH = "data/BESyllabus.pdf"  # change this
CHROMA_DIR = "chroma_db"

def get_embedding(text, task_type="retrieval_document"):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config=types.EmbedContentConfig(task_type=task_type)
    )
    return response.embeddings[0].values

def ingest():
    print("Loading PDF...")
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    print(f"Loaded {len(documents)} pages")

    print("Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks")

    print("Embedding and storing in ChromaDB...")
    db = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = db.get_or_create_collection("rag_docs")

    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk.page_content)
        collection.add(
            ids=[f"chunk_{i}"],
            embeddings=[embedding],
            documents=[chunk.page_content],
            metadatas=[chunk.metadata]
        )
        if (i + 1) % 50 == 0:
            print(f"  Stored {i+1}/{len(chunks)} chunks...")

    print("Done! Vectors saved to chroma_db/")

if __name__ == "__main__":
    ingest()