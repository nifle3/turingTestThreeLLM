from abc import ABC, abstractmethod

from models.judge import Judge
from models.player import Player


class Game(ABC):

    @abstractmethod
    def play(self) -> str:
        pass


class GameForTwoPlayer(Game):
    __slots__ = ("__judge", "__players")

    def __init__(self, players: tuple[Player, Player], judge: Judge) -> None:
        self.__players = players
        self.__judge = judge

    def play(self) -> str:
        question = self.__judge.init_start_question()

        while not self.__judge.have_result():
            first_answer = self.__players[0].answer(question)
            second_answer = self.__players[1].answer(question)

            question = self.__judge.generate_next_question(first_answer, second_answer)

        return self.__judge.get_result()
