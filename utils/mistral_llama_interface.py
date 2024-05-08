from langchain_community.llms.llamacpp   import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate


prompt = PromptTemplate.from_template("""
You are a helpful chatbot. Respond to questions like a human would
Question: {query}
""")

# Callbacks support token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])


mistral_7b = LlamaCpp(
    model_path="C:/Users/kvgk2/OneDrive/Desktop/Abhi/code/MandanGPT/models/7b/mistral-7b-v0.1.Q5_K_S.gguf",
    temperature=0.4,
    max_tokens=200,
    top_p=1,
    n_gpu_layers=33,
    n_ctx=1024,
    n_batch=512,
    # callback_manager=callback_manager,
    # verbose=True,  # Verbose is required to pass to the callback manager
)

if __name__ == "__main__":
    question = """
    Question: A rap battle between Stephen Colbert and John Oliver
    """

    response = llm.invoke(question)

    print(response)

