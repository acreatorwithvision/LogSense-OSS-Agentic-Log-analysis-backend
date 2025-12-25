from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load embedding model once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# FAISS index (cosine similarity)
dimension = 384
index = faiss.IndexFlatIP(dimension)

# Store original texts
documents = []

def add_documents(texts: list[str]):
    global documents

    embeddings = embedding_model.encode(texts, normalize_embeddings=True)
    embeddings = np.array(embeddings).astype("float32")

    index.add(embeddings)
    documents.extend(texts)

def search(query: str, top_k: int = 3):
    query_embedding = embedding_model.encode(
        [query], normalize_embeddings=True
    )
    query_embedding = np.array(query_embedding).astype("float32")

    scores, indices = index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        if idx < len(documents):
            results.append(documents[idx])

    return results
