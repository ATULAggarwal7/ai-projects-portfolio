from app.rag.guideline_loader import load_guidelines
from app.rag.vector_store import create_vector_store

JS_PATH = "guidelines/javascript_guidelines.md"
PY_PATH = "guidelines/python_guidelines.md"


def main():

    js_docs = load_guidelines(JS_PATH)
    py_docs = load_guidelines(PY_PATH)

    all_docs = js_docs + py_docs

    create_vector_store(all_docs)

    print("All guidelines stored in vector DB")


if __name__ == "__main__":
    main()