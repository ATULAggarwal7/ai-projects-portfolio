from llama_cpp import Llama


class LocalLLM:

    _instance = None

    @classmethod
    def get_model(cls):

        if cls._instance is None:

            print("Loading LLM model (only once)...")

            cls._instance = Llama(
                model_path=r"D:\LLM\Qwen2.5-7B-Instruct-Q5_K_M.gguf",               #Link to download LLM ( https://huggingface.co/bartowski/Qwen2.5-7B-Instruct-GGUF)
                n_ctx=4096,
                n_threads=8,
                n_gpu_layers=0,
                verbose=False
            )

            print("LLM loaded successfully")

        return cls._instance

    def generate(self, prompt):

        llm = self.get_model()

        response = llm(
            prompt,
            max_tokens=500,
            temperature=0.0,   # deterministic output
            top_p=0.9,
            stop=[
                "\n\n\n",
                "Explanation:",
                "Here is",
                "Sure",
                "The code review"
            ]
        )

        return response["choices"][0]["text"].strip()