from abc import ABC

from langchain.chat_models.base import BaseChatModel

class Judge(ABC):
    pass


class LangChainJudge(Judge):
    __slots__ = ("__model")

    def __init__(self, model: BaseChatModel) -> None:
        self.__model = model
