from os import getenv
from utils import llm_provider, llm_params, llm_config
from typing import Union
from utils import GeminiConfig, OllamaConfig, OpenAIConfig


llm_params: Union[GeminiConfig, OllamaConfig, OpenAIConfig]


def get_ollama_models():
    try:
        from langchain_ollama.embeddings import OllamaEmbeddings
        from langchain_ollama.chat_models import ChatOllama
    except ImportError:
        print("Please install the langchain-ollama package")
        exit(0)

    llm = ChatOllama(
        base_url=llm_params.url,
        model=llm_params.chat_model,
        temperature=0,
        seed=1234,
        num_ctx=500,
    ).configurable_fields(**llm_config)
    if llm_params.embeddings_model:
        embeddings = OllamaEmbeddings(
            base_url=llm_params.url, model=llm_params.embeddings_model
        )
    else:
        embeddings = None
    return llm, embeddings


def get_gemini_models():
    try:
        from langchain_google_genai import (
            ChatGoogleGenerativeAI,
            GoogleGenerativeAIEmbeddings,
        )
    except ImportError:
        print("Please install the langchain-google-genai package")
        exit(0)

    llm = ChatGoogleGenerativeAI(
        model=llm_params.chat_model,
        api_key=llm_params.api_key,
        temperature=0,
        max_tokens=100,
        timeout=None,
        max_retries=2,
    )
    if llm_params.embeddings_model:
        embeddings = GoogleGenerativeAIEmbeddings(model=llm_params.embeddings_model)
    else:
        embeddings = None
    return llm, embeddings


def get_openai_models():
    try:
        from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
    except ImportError:
        print("Please install the langchain-openai package")
        exit(0)

    llm = AzureChatOpenAI(
        deployment_name=llm_params.chat_model,
        temperature=0,
        max_tokens=500,
    )
    if llm_params.embeddings_model:
        embeddings = AzureOpenAIEmbeddings(
            azure_deployment=llm_params.embeddings_model,
        )
    else:
        embeddings = None
    return llm, embeddings


def get_transformer_models():
    try:
        from langchain_community.llms.vllm import VLLM

        from langchain_community.embeddings import Model2vecEmbeddings
    except ImportError:
        print("Please install the langchain-community package")
        exit(0)

    llm = VLLM(
        model=llm_params.chat_model,
        trust_remote_code=True,  # mandatory for hf models
        max_new_tokens=128,
        top_k=10,
        top_p=0.95,
        temperature=0.2,
    )
    if llm_params.embeddings_model:
        embeddings = Model2vecEmbeddings(
            llm_params.embeddings_model
        )
    return llm, embeddings


match llm_provider:
    case "ollama":
        func = get_ollama_models
    case "gemini":
        func = get_gemini_models
    case "opeani":
        func = get_openai_models
    case "vllm":
        func = get_transformer_models

llm, embeddings = func()
