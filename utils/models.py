from pydantic import BaseModel
from langchain_core.runnables import ConfigurableField
from typing import Optional


__all__ = [
    "OllamaConfig",
    "TranformerConfig",
    "GeminiConfig",
    "OpenAIConfig",
    "UsageMetaData",
    "HelpCmdArgs",
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


# Discord
# Help Commands
class HelpCmdArgs(BaseModel):
    cog_or_cmd_name: Optional[str] = None
    cog_name: Optional[str] = None
    cmd_name: Optional[str] = None


# Langchain ConfigurableField
temperature_config = ConfigurableField(
    id="temperature",
    name="LLM Temperature",
    description="Set model temperature",
)
num_ctx_config = ConfigurableField(
    id="num_ctx",
    name="Context Window",
    description="Set context window size",
)
max_tokens_config = ConfigurableField(
    id="max_tokens",
    name="Context Window",
    description="Set context window size",
)
seed_config = ConfigurableField(
    id="seed",
    name="Seed",
    description="Setting this to a specific number will make the model generate the same text for the same prompt.",
)
top_k_config = ConfigurableField(
    id="top_k",
    name="top k",
    description="Reduces the probability of generating nonsense. A higher value (e.g. 100) will give more diverse answers, while a lower value (e.g. 10) will be more conservative.",
)
top_p_config = ConfigurableField(
    id="top_p",
    name="top p",
    description="Works together with top-k. A higher value (e.g., 0.95) will lead to more diverse text, while a lower value (e.g., 0.5) will generate more focused and conservative text. ",
)

min_p_config = ConfigurableField(
    id="min_p",
    name="min p",
    description="Alternative to the top_p, and aims to ensure a balance of quality and variety. The parameter p represents the minimum probability for a token to be considered, relative to the probability of the most likely token. For example, with p=0.05 and the most likely token having a probability of 0.9, logits with a value less than 0.045 are filtered out.",
)
