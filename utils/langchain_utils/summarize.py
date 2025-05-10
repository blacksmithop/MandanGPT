from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from utils import llm, ChainInputInvalid
from .runnable_parser import get_content_and_metadata


prompt = ChatPromptTemplate.from_messages(
    [
        HumanMessagePromptTemplate.from_template("Write a concise summary of the following:```{context}```"),
    ]
)
# Gemini doesn't like system prompts, infer LLM type & switch chain?

summarize_chain = prompt | llm | get_content_and_metadata


async def summarize_text(text: str, temperature: float = 0.2, top_p: float = 0.9, num_ctx: int = 250):
    try:
        summary_text, usage_metadata = summarize_chain.invoke(
            {"context": text}, {"configurable": {"temperature": temperature, }}
        )
        return summary_text, usage_metadata
    except Exception as e:
        raise ChainInputInvalid
