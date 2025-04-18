from langchain_core.messages.ai import AIMessage
from utils.models import UsageMetaData


def get_content_and_metadata(message: AIMessage):
    print(type(message))
    print(message)
    content, metadata = message.content, UsageMetaData(**message.usage_metadata)
    return content, metadata