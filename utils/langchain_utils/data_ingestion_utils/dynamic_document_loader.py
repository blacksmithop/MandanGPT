from langchain_unstructured.document_loaders import UnstructuredLoader
from pathlib import Path
from typing import List


def load_documents_with_untructured(file_dir: List[Path]):
    loader = UnstructuredLoader(file_path=file_dir)
    docs_lazy = loader.lazy_load()
    ...