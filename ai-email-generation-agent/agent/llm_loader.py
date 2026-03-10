from llama_cpp import Llama
from config.settings import MODEL_PATH


class LLMLoader:
    def __init__(self):
        self.llm = Llama(
            model_path=MODEL_PATH,
            n_ctx=2048,          # context size
            n_threads=8,         # adjust based on your CPU cores
            n_batch=512,
            verbose=False
        )

    def generate(self, prompt: str, max_tokens: int = 300) -> str:
        response = self.llm(
            prompt,
            max_tokens=max_tokens,
            temperature=0.3,
            top_p=0.9,
            stop=["</s>"]
        )

        return response["choices"][0]["text"].strip()