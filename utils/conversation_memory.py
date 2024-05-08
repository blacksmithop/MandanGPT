from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from utils.ollama_interface import mistral_7b_ollama
# from utils.mistral_llama_interface import mistral_7b

store = {}

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an intelligent yet whimsical chatbot. Pretend to be a human and answer like a normal if slightly silly person.",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)
runnable = prompt | mistral_7b_ollama

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


with_message_history = RunnableWithMessageHistory(
    runnable,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)