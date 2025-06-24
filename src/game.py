from typing import Tuple
from abc import ABC, abstractmethod

from player import Player
from judge import Judge


class Game(ABC):

    @abstractmethod
    def play(self) -> str:
        pass


class GameForTwoPlayer(Game):
    __slots__ = ("__players", "__judge")

    def __init__(self, players: Tuple[Player, Player], judge: Judge) -> None:
        self.__players = players
        self.__judge = judge

    def play(self) -> str:
        question = self.__judge.init_start_question()

        while not self.__judge.have_result():
            first_answer = self.__players[0].answer(question)
            second_answer = self.__players[1].answer(question)

            question = self.__judge.generate_next_question(first_answer, second_answer)

        return self.__judge.get_result()
