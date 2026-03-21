import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain.embeddings.base import Embeddings
from groq import Groq
import numpy as np

load_dotenv()

CHROMA_DIR = "chroma_db"
client = Groq()

class GroqEmbeddings(Embeddings):
    """Lightweight embedding class using a small local model via Groq."""
    
    def __init__(self):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
    
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts, show_progress_bar=False).tolist()
    
    def embed_query(self, text: str) -> list[float]:
        return self.model.encode([text], show_progress_bar=False)[0].tolist()

embeddings = GroqEmbeddings()
vector_store = Chroma(
    persist_directory=CHROMA_DIR,
    embedding_function=embeddings
)

def query(question: str, top_k: int = 3) -> dict:
    results = vector_store.similarity_search(question, k=top_k)
    context = "\n\n".join([r.page_content for r in results])
    sources = list(set([r.metadata["source"] for r in results]))

    prompt = f"""You are a smart TV telemetry expert assistant.
Use the following documentation to answer the question.
If the answer is not in the documentation, say "I don't have information about that."

Documentation:
{context}

Question: {question}

Answer clearly and concisely."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "question": question,
        "answer": response.choices[0].message.content,
        "sources": sources,
        "context_used": context
    }