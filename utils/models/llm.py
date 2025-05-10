from pydantic import BaseModel
from typing import Optional

__all__ = [
    "OllamaConfig",
    "TranformerConfig",
    "GeminiConfig",
    "OpenAIConfig",
    "UsageMetaData",
]

# LLM
class OllamaConfig(BaseModel):
    url: str
    chat_model: str
    embeddings_model: Optional[str] = None


class TranformerConfig(BaseModel):
    url: str
    chat_model: str
    embeddings_model: Optional[str] = None


class GeminiConfig(BaseModel):
    api_key: str
    chat_model: str
    embeddings_model: Optional[str] = None


class OpenAIConfig(BaseModel):
    api_key: str
    api_version: str
    api_endpoint: str
    chat_model: str
    embeddings_model: Optional[str] = None

# Usage Metadata
class UsageMetaData(BaseModel):
    input_tokens: int
    output_tokens: int
    total_tokens: int