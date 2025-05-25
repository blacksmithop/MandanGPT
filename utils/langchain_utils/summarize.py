from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from .runnable_parser import get_content_and_metadata
from utils import ChainInputInvalid, langfuse_handler #, llm_model
from utils.langchain_utils.llm_core import llm_model


prompt = ChatPromptTemplate.from_messages(
    [
        HumanMessagePromptTemplate.from_template(
            "Write a concise summary of the following:```{context}```"
        ),
    ]
)
# Gemini doesn't like system prompts, infer LLM type & switch chain?

summarize_chain = prompt |llm_model | get_content_and_metadata


async def summarize_text(
    text: str,
    temperature: float = 0.2,
    top_p: float = 0.9,
    top_k: int = 40,
    num_ctx: int = 250,
):
    try:
        summary_text, usage_metadata = await summarize_chain.ainvoke(
            input={"context": text},
            config=
            {
                "callbacks": [langfuse_handler],
                "configurable": {
                    "temperature": temperature,
                    "num_ctx": num_ctx,
                    "top_p": top_p,
                    "top_k": top_k,
                }
            }
        )
        return summary_text, usage_metadata
    except Exception as e:
        raise ChainInputInvalid
