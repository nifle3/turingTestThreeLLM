from abc import ABC, abstractmethod
from typing import Generator

from models.judge import Judge
from models.player import Player


class TuringTest(ABC):
    """Strategy for turing test."""

    @abstractmethod
    def start(self) -> Generator[str, None, str]:
        """Start turing test."""


class TuringTestForTwoPlayer(TuringTest):
    """Turing test for two player with same question for players."""

    __slots__ = ("_judge", "_players")

    def __init__(self, players: tuple[Player, Player], judge: Judge) -> None:
        """Constructor."""
        self._players = players
        self._judge = judge

    def start(self) -> Generator[str, None, str]:
        """Start turing test."""
        question = self._judge.init_start_question()

        while not self._judge.have_result():
            yield f"judge: {question}"

            first_answer = self._players[0].answer(question)
            second_answer = self._players[1].answer(question)

            yield f"first: {first_answer}"
            yield f"second: {second_answer}"


            question = self._judge.generate_next_question(first_answer, second_answer)

        return f"Результат: {self._judge.player_that_human}"
