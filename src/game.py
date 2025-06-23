from typing import Tuple

from player import Player
from judge import Judge

class Game:
    __slots__ = ("__players", "__judge")

    def __init__(self, players: Tuple[Player, Player], judge: Judge) -> None:
        self.__players = players
        self.__judge = judge

    def play(self) -> None:
        pass
