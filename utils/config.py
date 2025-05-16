from os import getenv, path
from utils import InvalidLLMProvider, MissingLLMProvider, TokenNotSet
from utils import GeminiConfig, OllamaConfig, OpenAIConfig, TranformerConfig
from utils import (
    seed_config,
    min_p_config,
    max_tokens_config,
    top_k_config,
    top_p_config,
    num_ctx_config,
    temperature_config,
)
import json
import sys


if discord_bot_token := getenv("DISCORD_BOT_TOKEN"):
    print("Loaded bot token from environment variables")
else:
    print("Failed to load bot token")
    raise TokenNotSet("Could not read Discord bot token")


if not path.isfile(f"./config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open(f"./config.json") as file:
        bot_config = json.load(file)


if llm_provider := getenv("LLM_PROVIDER"):
    match llm_provider:
        case "ollama":
            llm_params = OllamaConfig(
                url=getenv("OLLAMA_URL"),
                chat_model=getenv("OLLAMA_CHAT_MODEL"),
                embeddings_model=getenv("OLLAMA_EMBEDDINGS_MODEL"),
            )
            llm_config = {
                "temperature": temperature_config,
                "num_ctx": num_ctx_config,
                # "seed": seed_config,
                "top_k": top_k_config,
                "top_p": top_p_config,
                # "min_p": min_p_config
            }
        case "transformers":
            llm_params = TranformerConfig(
                url=getenv("VLLM_URL"),
                chat_model=getenv("VLLM_CHAT_MODEL"),
                embeddings_model=getenv("MODEL2VEC_EMBEDDING_MODEL"),
            )
            llm_config = {
                "temperature": temperature_config,
                "max_tokens": max_tokens_config,
            }
        case "gemini":
            llm_params = GeminiConfig(
                api_key=getenv("GOOGLE_API_KEY"),
                chat_model=getenv("GOOGLE_CHAT_MODEL"),
                embeddings_model=getenv("GOOGLE_EMBEDDINGS_MODEL"),
            )
            llm_config = {
                "temperature": temperature_config,
            }
        case "openai":
            llm_params = OpenAIConfig(
                api_key=getenv("AZURE_OPENAI_API_KEY"),
                api_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
                api_version=getenv("AZURE_OPENAI_API_VERSION"),
                chat_model=getenv("OLLAMA_CHAT_MODEL"),
                embeddings_model=getenv("OLLAMA_EMBEDDINGS_MODEL"),
            )
            llm_config = {
                "temperature": temperature_config,
            }
        case _:
            raise InvalidLLMProvider("LLM Provider is not valid")
else:
    raise MissingLLMProvider("LLM Provider was not set")
