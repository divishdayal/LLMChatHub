import logging
import tempfile
from typing import List, Optional

from langchain import ConversationChain, LLMChain, OpenAI, PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import SeleniumURLLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ChatMessageHistory, ConversationBufferWindowMemory
from langchain.vectorstores import Chroma

import src.models as models
from src.config import api_config
from src.constants import PROMPT

logger = logging.getLogger(__name__)


class ChatBot:
    def __init__(
        self,
        text_files: Optional[List[str]] = [],
        urls: Optional[List[str]] = [],
    ):
        self._loaders = []
        self._chain = None
        self._msg_history = None
        self._add_loaders(text_files, urls)

    def _add_loaders(self, text_files: List[str], urls: List[str]) -> List:
        for file_path in text_files:
            self._loaders.append(TextLoader(file_path))

        if len(urls) > 0:
            loader = SeleniumURLLoader(urls=urls)
            self._loaders.append(loader)

        vectorstore = None
        if len(self._loaders) > 0:
            docs = []
            for loader in self._loaders:
                docs.extend(loader.load())

            embeddings = OpenAIEmbeddings()
            vectorstore = Chroma.from_documents(docs, embeddings)
        self._vectorstore = vectorstore

    def _compute_msg_history(self, messages: List[models.Message]):
        _msg_history = ChatMessageHistory()
        for m in messages:
            if m.is_ai:
                _msg_history.add_ai_message(m.message)
            else:
                _msg_history.add_user_message(m.message)
        self._msg_history = _msg_history

    def add_text_loader(self, text_files: List[str]):
        self._add_loaders(text_files, [])

    def add_url_loader(self, urls: List[str]):
        self._add_loaders([], urls)

    def generate(
        self,
        query: str,
        messages: Optional[List[models.Message]] = [],
        mock_generate: Optional[bool] = api_config.MOCK_GENERATE,
    ) -> str:
        """
        :param query: what to ask
        :param text_files:
        :param urls:
        :param messages:
        :return:
        """
        if mock_generate:
            return "mock response"

        if len(messages) > 0:
            self._compute_msg_history(messages)

        if self._vectorstore is not None:
            # ConversationalRetrievalChain can only be used with docs/vectorstore
            kwargs = {
                "llm": OpenAI(temperature=0),
                "retriever": self._vectorstore.as_retriever(),
            }
            if self._msg_history is not None:
                kwargs["memory"] = self._msg_history
            else:
                kwargs["memory"] = ConversationBufferWindowMemory(
                    k=2, memory_key="chat_history", return_messages=False
                )
            qa = ConversationalRetrievalChain.from_llm(
                **kwargs,
            )
            result = qa({"question": query})
            response = result["answer"]
        else:
            # to use without vectorstore docs
            prompt = PromptTemplate(
                input_variables=["history", "human_input"], template=PROMPT
            )
            kwargs = {
                "llm": OpenAI(temperature=0),
                "verbose": False,
                "prompt": prompt,
                "memory": ConversationBufferWindowMemory(k=2),
            }
            if self._msg_history is not None:
                kwargs["memory"] = self._msg_history
            conv_chain = LLMChain(
                **kwargs,
            )
            response = conv_chain.predict(human_input=query)

        return response


if __name__ == "__main__":
    cb = ChatBot()

    # Example 1
    # cb.add_url_loader(["https://python.langchain.com/en/latest/index.html"])
    # print(cb.generate("The LangChain framework is designed for what?"))

    # Example 2
    temp = tempfile.NamedTemporaryFile()
    with open(temp.name, "w") as f:
        f.write("lite is a popular slang in bits pilani.")
    cb.add_text_loader([temp.name])
    print(cb.generate("give me a slang of bits pilani?"))
