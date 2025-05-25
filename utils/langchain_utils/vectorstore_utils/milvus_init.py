from langchain_milvus import Milvus
from os import getenv
from utils.langchain_utils.llm_core import embeddings
from utils.langchain_utils.vectorstore_utils import find_or_create_database

MILVUS_HOST, MILVUS_PORT = getenv("MILVUS_HOST"), getenv("MILVUS_PORT")
MILVUS_URI = f"http://{MILVUS_HOST}:{MILVUS_PORT}"
MILVUS_USER, MILVUS_PWD = getenv("MILVUS_USERNAME"), getenv("MILVUS_PWD")
MILVUS_DB_NAME = getenv("MILVUS_DATABASE")
MILVUS_TOKEN = f"{MILVUS_USER}:{MILVUS_PWD}"

find_or_create_database(milvus_host=MILVUS_HOST, milvus_port=MILVUS_PORT, token=MILVUS_TOKEN, db_name=MILVUS_DB_NAME)

milvus_vectorstore = Milvus(
    embedding_function=embeddings,
    connection_args={"uri": MILVUS_URI, "token": MILVUS_TOKEN, "db_name": MILVUS_DB_NAME},
    index_params={"index_type": "FLAT", "metric_type": "L2"},
    consistency_level="Strong",
    drop_old=False,
)

milvus_retriever = milvus_vectorstore.as_retriever()
