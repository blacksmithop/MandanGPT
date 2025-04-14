from langchain_core.prompts import ChatPromptTemplate
from utils import llm, ChainInputInvalid
from .runnable_parser import get_content_and_metadata


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Write a concise summary of the following:```{context}```"),
    ]
)

summarize_chain = prompt | llm | get_content_and_metadata


async def summarize_text(text: str, temperature: float = 0.2, top_p: float = 0.9, num_ctx: int = 250):
    try:
        summary_text, usage_metadata = summarize_chain.invoke(
            {"context": text}, {"configurable": {"temperature": temperature, "num_ctx": num_ctx}} # TODO: Top P, other params
        )
        return summary_text, usage_metadata
    except Exception as e:
        print(e)
        raise ChainInputInvalid
