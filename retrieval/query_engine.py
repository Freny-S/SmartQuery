import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from groq import Groq

load_dotenv()

CHROMA_DIR = "chroma_db"
client = Groq()

def load_vector_store():
    """Load the existing ChromaDB vector store."""
    embeddings = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    vector_store = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )
    return vector_store

def query(question: str, top_k: int = 3) -> dict:
    """
    Retrieve relevant chunks and generate an answer.
    """
    vector_store = load_vector_store()

    # Step 1: Find most relevant chunks
    results = vector_store.similarity_search(question, k=top_k)
    context = "\n\n".join([r.page_content for r in results])
    sources = list(set([r.metadata["source"] for r in results]))

    # Step 2: Send context + question to LLM
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

if __name__ == "__main__":
    print("Testing query engine...\n")
    result = query("What fields does a BufferingEvent contain?")
    print(f"Question: {result['question']}")
    print(f"\nAnswer: {result['answer']}")
    print(f"\nSources: {result['sources']}")