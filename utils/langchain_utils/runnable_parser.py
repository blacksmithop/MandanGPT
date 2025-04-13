from langchain_core.messages.ai import AIMessage
from utils.models import UsageMetaData


def get_content_and_metadata(message: AIMessage):
    content, metadata = message.content, UsageMetaData(**message.usage_metadata)
    metadata_message = f"Input: {metadata.input_tokens} tokens | Output: {metadata.output_tokens} tokens | Total: {metadata.total_tokens} tokens"
    return content, metadata_message