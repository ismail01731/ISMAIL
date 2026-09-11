import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction


# Local embedding model
embedding_function = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)


# Chroma persistent database
client = chromadb.PersistentClient(
    path="./database"
)


# Universal AI collection
collection = client.get_or_create_collection(
    name="universal_ai",
    embedding_function=embedding_function
)