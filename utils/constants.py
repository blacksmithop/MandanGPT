from os import getenv
from utils import InvalidLLMProvider, MissingLLMProvider, TokenNotSet
from utils import GeminiConfig, OllamaConfig, OpenAIConfig

if discord_bot_token:= getenv("DISCORD_BOT_TOKEN"):
    print("Loaded bot token from environment variables")
else:
    print("Failed to load bot token")
    raise TokenNotSet("Could not read Discord bot token")


if llm_provider:= getenv("LLM_PROVIDER"):
    match llm_provider:
        case "ollama":
            llm_config = OllamaConfig(
                url=getenv("OLLAMA_URL"),
                chat_model=getenv("OLLAMA_CHAT_MODEL"),
                embeddings_model=getenv("OLLAMA_EMBEDDINGS_MODEL")
            )
        case "gemini":
            llm_config = GeminiConfig(
                api_key=getenv("GOOGLE_API_KEY"),
                chat_model=getenv("OLLAMA_CHAT_MODEL"),
                embeddings_model=getenv("OLLAMA_EMBEDDINGS_MODEL")
            )
        case "openai":
            llm_config = OpenAIConfig(
                api_key=getenv("AZURE_OPENAI_API_KEY"),
                api_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
                api_version=getenv("AZURE_OPENAI_API_VERSION"),
                chat_model=getenv("OLLAMA_CHAT_MODEL"),
                embeddings_model=getenv("OLLAMA_EMBEDDINGS_MODEL")
            )
        case _:
            raise InvalidLLMProvider("LLM Provider is not valid")
else:
    raise MissingLLMProvider("LLM Provider was not set")