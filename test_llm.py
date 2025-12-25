from llama_cpp import Llama

llm = Llama(
    model_path="models/models/phi-2.Q4_K_M.gguf",
    n_ctx=512
)

response = llm(
    "Explain log aggregation in simple terms.",
    max_tokens=100
)

print(response["choices"][0]["text"])
