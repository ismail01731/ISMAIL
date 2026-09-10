import chromadb

client = chromadb.PersistentClient(path="./database")

collection = client.get_or_create_collection(
    name="universal_ai"
)