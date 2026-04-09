import os
import chromadb
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
CHROMA_DIR = "chroma_db"

def ask(question: str):
    db = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = db.get_collection("rag_docs")

    query_embedding_response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=question,
        config=types.EmbedContentConfig(task_type="retrieval_query")
    )
    query_embedding = query_embedding_response.embeddings[0].values

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

Question: {question}

Answer:"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    print("\n--- Answer ---")
    print(response.text)
    print("\n--- Sources used ---")
    for i, (chunk, meta) in enumerate(zip(context_chunks, sources)):
        print(f"\nSource {i+1} | Page {meta.get('page', '?')}:")
        print(chunk[:150] + "...")

if __name__ == "__main__":
    q = input("Ask a question: ")
    ask(q)