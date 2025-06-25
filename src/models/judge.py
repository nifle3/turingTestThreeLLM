from abc import ABC, abstractmethod
from typing import final

from langchain.chat_models.base import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage

from .errors import InvalidOutputLLMError


@final
class ResultIsNotReadyError(Exception):
    pass


class Judge(ABC):

    @abstractmethod
    def init_start_question(self) -> str:
        pass

    @abstractmethod
    def generate_next_question(self, first_answer: str, second_answer: str) -> str:
        pass

    @abstractmethod
    def have_result(self) -> bool:
        pass

    @abstractmethod
    def get_result(self) -> str:
        pass


@final
class LangChainJudge(Judge):
    __slots__ = ("__memory", "__model", "__result")

    def __init__(self, model: BaseChatModel, system_prompt: str) -> None:
        self.__memory: list[BaseMessage] = [SystemMessage(system_prompt)]
        self.__model: BaseChatModel = model
        self.__result: str | None = None

    def init_start_question(self) -> str:
        message = self.__model.invoke(self.__memory)

        if not isinstance(message.content, str):
            raise InvalidOutputLLMError()

        self.__memory.append(AIMessage(message.content))

        return message.content

    def generate_next_question(self, first_answer: str, second_answer: str) -> str:
        self.__memory.append(HumanMessage(f"first - {first_answer}"))
        self.__memory.append(HumanMessage(f"second - {second_answer}"))

        message = self.__model.invoke(self.__memory)

        if not isinstance(message.content, str):
            raise InvalidOutputLLMError()

        self.__memory.append(AIMessage(message.content))

        return message.content

    def have_result(self) -> bool:
        return self.__result is not None

    def get_result(self) -> str:
        if self.__result is None:
            raise ResultIsNotReadyError

        return self.__result
