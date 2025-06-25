from abc import ABC, abstractmethod
from typing import final

from model_metadata import ModelMetadata

from rich.console import Console


@final
class InvalidInputIndexError(Exception):
    """Exception for digit out of index."""


@final
class InvalidInputTypeError(Exception):
    """Exception for non digit input."""


class UserAsker(ABC):
    """Abstract class for interact user."""

    @abstractmethod
    def ask(self, title: str) -> ModelMetadata:
        """Abstract method for ask user."""


@final
class DefaultUserAsker(UserAsker):
    """Class for interact with user to define model to use."""

    __slots__ = ("_model_metadatas", "_console")

    def __init__(self, model_metadatas: list[ModelMetadata], console: Console) -> None:
        """Constructor."""
        self._model_metadatas: list[ModelMetadata] = model_metadatas
        self._console = console

    def ask(self, title: str) -> ModelMetadata:
        """Ask user via cli and user input which model want to user."""
        raise NotImplementedError

    def _print(self, title: str) -> None:
        self._console.print(title)

        for index, model_metadata in enumerate(self._model_metadatas):
            self._console.print(f"{index} - {model_metadata}")

    def _input(self) -> ModelMetadata:
        user_input = self._console.input("Ваш выбор: ")
        if not user_input.strip().isdigit():
            raise InvalidInputTypeError

        user_int_input = int(user_input)

        if user_int_input > len(self._model_metadatas):
            raise InvalidInputIndexError

        return self._model_metadatas[user_int_input]
