from langfuse.callback import CallbackHandler
from os import getenv

langfuse_handler = CallbackHandler(
    secret_key=getenv("LANGFUSE_SECRET_KEYs"),
    public_key=getenv("LANGFUSE_PUBLIC_KEY"),
    host=getenv("LANGFUSE_HOST")
)

