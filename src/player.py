from abc import ABC
from typing import final

from langchain.chat_models.base import BaseChatModel


class Player(ABC):
    pass

@final
class LangChainPlayer(Player):
    __slots__ = ("__model")


    def __init__(self, model: BaseChatModel) -> None:
        self.__model = model
