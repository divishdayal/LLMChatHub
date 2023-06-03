import logging
from typing import List, Optional, Tuple

from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader, SeleniumURLLoader
from langchain.indexes import VectorstoreIndexCreator

logger = logging.getLogger(__name__)



def _add_loaders(text_files: List[str], urls: List[str]) -> List:
    loaders = []
    for file_path in text_files:
        loaders.append(TextLoader(file_path))

    if len(urls) > 0:
        loader = SeleniumURLLoader(urls=urls)
        loaders.append(loader)

    return loaders


def chat(
    query: str, text_files: Optional[List[str]] = [], urls: Optional[List[str]] = []
) -> str:
    """
    :param query: what to ask
    :param text_files:
    :param urls:
    :return:
    """

    loaders = _add_loaders(text_files, urls)

    if len(loaders) > 0:
        index = VectorstoreIndexCreator().from_loaders(loaders)
        response = str(index.query_with_sources(query)["answer"])
    else:
        llm = ChatOpenAI(temperature=0.5, model_name="gpt-3.5-turbo")
        response = str(llm.predict(query))

    return response


if __name__ == "__main__":
    chat(
        query="When was Japan first inhabited?",
        urls=[
            "https://en.wikipedia.org/wiki/Japan",
        ],
    )
