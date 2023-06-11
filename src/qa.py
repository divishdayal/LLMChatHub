import logging
from typing import List, Optional

from langchain import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import SeleniumURLLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.memory import ChatMessageHistory
from langchain.vectorstores import Chroma

import src.models as models

logger = logging.getLogger(__name__)


def _add_loaders(text_files: List[str], urls: List[str]) -> List:
    loaders = []
    for file_path in text_files:
        loaders.append(TextLoader(file_path))

    if len(urls) > 0:
        loader = SeleniumURLLoader(urls=urls)
        loaders.append(loader)

    return loaders


def _get_message_history(messages: List[models.Message]) -> ChatMessageHistory:
    history = ChatMessageHistory()
    for m in messages:
        if m.is_ai:
            history.add_ai_message(m.message)
        else:
            history.add_user_message(m.message)
    return history


def generate(
    query: str,
    text_files: Optional[List[str]] = [],
    urls: Optional[List[str]] = [],
    messages: Optional[List[models.Message]] = [],
) -> str:
    """
    :param query: what to ask
    :param text_files:
    :param urls:
    :param messages:
    :return:
    """

    loaders = _add_loaders(text_files, urls)

    vectorstore = None
    memory = None

    if len(loaders) > 0:
        docs = []
        for loader in loaders:
            docs.extend(loader.load())

        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma.from_documents(docs, embeddings)

    if len(messages) > 0:
        memory = _get_message_history(messages)

    kwargs = {
        "llm": OpenAI(temperature=0),
    }
    if memory is not None:
        kwargs["memory"] = memory
    if vectorstore is not None:
        kwargs["vectorstore"] = vectorstore.as_retriever()
    qa = ConversationalRetrievalChain.from_llm(
        **kwargs,
    )
    result = qa({"question": query})
    response = result["answer"]

    return response


if __name__ == "__main__":
    response = generate(
        query="When was Japan first inhabited?",
        urls=[
            "https://en.wikipedia.org/wiki/Japan",
        ],
    )
    print(response)
