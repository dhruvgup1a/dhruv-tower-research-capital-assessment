import chromadb
from src.config import *
from sentence_transformers import SentenceTransformer
import json

# Use for embedding chunks
class SentenceTransformerEmbeddings:
    def __init__(self, model_name="all-MiniLM-L12-v2"):
        self.model = SentenceTransformer(model_name)
    
    def embed_query(self, query):
        return self.model.encode([query], convert_to_numpy=True)[0]
    
    def embed_chunks(self, chunks):
        return self.model.encode(chunks, convert_to_numpy=True)

# Produces normalized vectors already
embeddings = SentenceTransformerEmbeddings()

chroma_client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
collection = chroma_client.get_or_create_collection(name="book_passages", metadata={"hnsw:space": "cosine"})

def create_chroma_index(chunks):
    """
    Stores chunks in vector DB. 
    """

    # combines all chunks
    texts = [chunk["text"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]
    ids = [chunk["id"] for chunk in chunks]

    # Embedding all chunks here
    embedded_chunks = embeddings.embed_chunks(texts)

    # Stores all chunks in DB
    collection.add(
        ids=ids,  
        embeddings=embedded_chunks.tolist(), 
        metadatas=metadatas, 
        documents=texts 
    )


def retrieve_relevant_passages(query, top_k=TOP_K_RETRIEVAL, filter_book=None):
    """
    Retrieves most releveant passages to theme using cosine similarity search. 
    """
    query_vector = embeddings.embed_query(query)

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        where={"book": filter_book} if filter_book else None
    )

    formatted_results = zip(results["ids"][0], results["documents"][0], results["metadatas"][0], results["distances"][0])

    passages = []
    for id, text, meta, score in formatted_results:
        
        similarity_percentage = round(score * 100, 2)

        formatted_result = { 
            "text": text,
            "metadata": {
                "id": id,
                "book": meta.get("book", "Unknown"),
                "chapter": meta.get("chapter", "Unknown"),
                "similarity_percentage": similarity_percentage
            }
        }
        passages.append(formatted_result)

    with open(f"{JSON_PATH}/{passages[0]['metadata']['book']}_top_chunks.json", "w") as f:
        json.dump(passages, f, indent=4)
