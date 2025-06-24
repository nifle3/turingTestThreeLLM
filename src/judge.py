from abc import ABC, abstractmethod
from typing import final

from langchain.chat_models.base import BaseChatModel

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
    __slots__ = ("__model", "__result")

    def __init__(self, model: BaseChatModel) -> None:
        self.__model: BaseChatModel = model
        self.__result: str | None = None

    def init_start_question(self) -> str:
        raise NotImplementedError()

    def generate_next_question(self, first_answer: str, second_answer: str) -> str:
        raise NotImplementedError()

    def have_result(self) -> bool:
        return self.__result is not None

    def get_result(self) -> str:
        if self.__result is None:
            raise ResultIsNotReadyError()

        return self.__result
