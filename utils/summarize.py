from utils import ChainInputInvalid
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils import llm

template = ChatPromptTemplate.from_template("Summarize this content: {text}")

summarize_chain = template | llm | StrOutputParser()


def get_summary(text: str):
    try:
        summary = summarize_chain.invoke({
            "text": text
        })
        return summary
    except Exception as e:
        print(e)
        raise ChainInputInvalid 
