from abc import ABC

from langchain.chat_models.base import BaseChatModel


class Player(ABC):
    pass


class LangChainPlayer(Player):
    __slots__ = ("__model")


    def __init__(self, model: BaseChatModel) -> None:
        self.__model = model
