# markdown file
#       ↓
# split into chunks
#       ↓
# each chunk stored in vector DB


from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

VECTOR_DB_PATH = "vector_db"


def get_embedding_model():
    """
    Load embedding model
    """

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return embeddings


def create_vector_store(documents):
    """
    Create and persist vector database
    """

    embeddings = get_embedding_model()

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=VECTOR_DB_PATH
    )

    vector_store.persist()

    return vector_store


def load_vector_store():
    """
    Load existing vector database
    """

    embeddings = get_embedding_model()

    vector_store = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings
    )

    return vector_store