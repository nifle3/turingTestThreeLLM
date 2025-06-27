from abc import ABC, abstractmethod
from typing import Iterable

from rich.console import Console

class Printer(ABC):
    """Class for printing ai message."""

    @abstractmethod
    def start_output(self, data_to_out: Iterable[str]) -> None:
        pass


class RichPrinter(Printer):
    __slots__ = ("_console",)

    def __init__(self, console: Console):
        self._console = console

    def start_output(self, data_to_out: Iterable[str]) -> None:
        for text in data_to_out:
            self._console.print(text)
