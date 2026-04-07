import threading
from utils.logger import logger


def get_user_input(prompt, timeout=30):
    user_input = [None]

    def ask():
        user_input[0] = input(prompt)

    thread = threading.Thread(target=ask)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        logger.warning("HITL timeout — no response")
        return None

    return user_input[0]