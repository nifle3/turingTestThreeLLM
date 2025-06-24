from abc import ABC, abstractmethod
from typing import final

from model_metadata import ModelMetadata

@final
class InvalidInputIndexError(Exception):
    pass

@final
class InvalidInputTypeError(Exception):
    pass

class UserAsker(ABC):
    @abstractmethod
    def __init__(self, model_metadatas: list[ModelMetadata]) -> None:
        pass

    @abstractmethod
    def print(self, title: str) -> None:
        pass

    @abstractmethod
    def input(self) -> ModelMetadata:
        pass

@final
class DefaultUserAsker(UserAsker):

    def __init__(self, model_metadatas: list[ModelMetadata]) -> None:
        self.__model_metadatas: list[ModelMetadata] = model_metadatas

    def print(self, title: str) -> None:
        print(title)

        for index, value in enumerate(self.__model_metadatas):
            print(f"{index} - {value}")

    def input(self) -> ModelMetadata:
        user_input = input("Ваш выбор: ")
        if not user_input.strip().isdigit():
            raise InvalidInputTypeError()

        user_int_input = int(user_input)

        if user_int_input > len(self.__model_metadatas):
            raise InvalidInputIndexError()

        return self.__model_metadatas[user_int_input]
