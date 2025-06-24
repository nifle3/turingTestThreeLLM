from abc import ABC, abstractmethod
from typing import final

from langchain.chat_models.base import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, BaseMessage


class Player(ABC):

    @abstractmethod
    def answer(self, question: str) -> str:
        pass

@final
class LangChainPlayer(Player):
    __slots__ = ("__model", "__memory")

    def __init__(self, model: BaseChatModel, system_prompt: str) -> None:
        self.__model = model
        self.__memory: list[BaseMessage] = [SystemMessage(system_prompt)]

    def answer(self, question: str) -> str:
        self.__memory.append(HumanMessage(question))
        message = self.__model.invoke(self.__memory)
        if not isinstance(message.content, str):
            raise InvalidOutputLLMError()

        self.__memory.append(AIMessage(message.content))
        return message.content
