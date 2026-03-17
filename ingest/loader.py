import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

load_dotenv()

DATA_DIR = Path("data")
CHROMA_DIR = "chroma_db"

def load_documents() -> list[dict]:
    """Read all .md and .txt files from the data directory."""
    docs = []
    for filepath in DATA_DIR.rglob("*.md"):
        text = filepath.read_text(encoding="utf-8")
        docs.append({
            "text": text,
            "source": str(filepath)
        })
    for filepath in DATA_DIR.rglob("*.txt"):
        text = filepath.read_text(encoding="utf-8")
        docs.append({
            "text": text,
            "source": str(filepath)
        })
    print(f"Loaded {len(docs)} document(s)")
    return docs

def chunk_documents(docs: list[dict]) -> list:
    """Split documents into smaller chunks for better retrieval."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = []
    for doc in docs:
        splits = splitter.create_documents(
            texts=[doc["text"]],
            metadatas=[{"source": doc["source"]}]
        )
        chunks.extend(splits)
    print(f"Created {len(chunks)} chunk(s)")
    return chunks

def build_vector_store(chunks: list):
    """Embed chunks and store in ChromaDB."""
    embeddings = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )
    print(f"Vector store built and saved to '{CHROMA_DIR}/'")
    return vector_store

if __name__ == "__main__":
    print("Starting ingestion pipeline...\n")
    docs = load_documents()
    chunks = chunk_documents(docs)
    build_vector_store(chunks)
    print("\nIngestion complete!")