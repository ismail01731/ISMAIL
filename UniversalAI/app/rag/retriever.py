from app.rag.vector_store import collection


def save_document(doc_id, text):

    try:
        collection.add(
            ids=[doc_id],
            documents=[text]
        )
        return True

    except Exception as e:
        print("Vector Save Error:", e)
        return False


def search_document(query):

    result = collection.query(
        query_texts=[query],
        n_results=3
    )

    return result