import os


def detect_language(filename: str):
    """
    Detect programming language based on file extension
    """

    ext = os.path.splitext(filename)[1]

    if ext == ".py":
        return "python"

    if ext in [".js", ".jsx"]:
        return "javascript"

    return "unknown"


def read_code_file(file_bytes):
    """
    Convert uploaded file bytes to string
    """

    code = file_bytes.decode("utf-8")

    return code