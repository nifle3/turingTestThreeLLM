from abc import ABC, abstractmethod, abstractproperty
from typing import final

from langchain.chat_models.base import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage

from models.errors import InvalidOutputLLMError


@final
class ResultIsNotReadyError(Exception):
    """Exception raised when attempting to retrieve a result that has not yet been determined."""


class Judge(ABC):
    """Abstract class representing an entity capable of generating questions and a result."""

    @abstractmethod
    def init_start_question(self) -> str:
        """
        Generates the initial question to start the evaluation process.

        Returns:
            str: The initial question.

        """

    @abstractmethod
    def generate_next_question(self, first_answer: str, second_answer: str) -> str:
        """
        Generates the next question based on the provided answers.

        Args:
            first_answer (str): Answer from the first participant.
            second_answer (str): Answer from the second participant.

        Returns:
            str: The next question.

        """

    @abstractmethod
    def have_result(self) -> bool:
        """
        Indicates whether the final result has been determined.

        Returns:
            bool: True if result is ready, False otherwise.

        """

    @abstractproperty
    def player_that_human(self) -> str:
        """
        Returns the final result of the evaluation.

        Returns:
            str: The final result.

        Raises:
            ResultIsNotReadyError: If the result is not yet available.

        """


@final
class LangChainJudge(Judge):
    """
    LangChain-based implementation of the Judge interface.

    Uses a chat model to ask questions and evaluate answers.

    Attributes:
        __memory (list[BaseMessage]): Conversation history with system, human, and AI messages.
        __model (BaseChatModel): The underlying LangChain chat model.
        __result (str | None): The final result, if available.

    """

    __slots__ = ("_memory", "_model", "_player_that_human")

    def __init__(self, model: BaseChatModel, system_prompt: str) -> None:
        """
        Initializes the LangChainJudge with a chat model and system prompt.

        Args:
            model (BaseChatModel): LangChain-compatible chat model.
            system_prompt (str): Initial system message to guide the model's behavior.

        """
        self._memory: list[BaseMessage] = [SystemMessage(system_prompt)]
        self._model: BaseChatModel = model
        self._player_that_human: str | None = None

    def init_start_question(self) -> str:
        """
        Generates the initial question using the model.

        Returns:
            str: The initial question.

        Raises:
            InvalidOutputLLMError: If the model returns an invalid output.

        """
        message = self._model.invoke(self._memory)

        if not isinstance(message.content, str):
            raise InvalidOutputLLMError

        self._memory.append(AIMessage(message.content))

        return message.content

    def generate_next_question(self, first_answer: str, second_answer: str) -> str:
        """
        Generates the next question based on two participant answers.

        Args:
            first_answer (str): Answer from the first participant.
            second_answer (str): Answer from the second participant.

        Returns:
            str: The generated follow-up question.

        Raises:
            InvalidOutputLLMError: If the model returns an invalid output.

        """
        self._memory.append(HumanMessage(f"first - {first_answer}"))
        self._memory.append(HumanMessage(f"second - {second_answer}"))

        message = self._model.invoke(self._memory)

        if not isinstance(message.content, str):
            raise InvalidOutputLLMError

        self._memory.append(AIMessage(message.content))

        return message.content

    def have_result(self) -> bool:
        """
        Checks whether a final result has been determined.

        Returns:
            bool: True if a result is available, False otherwise.

        """
        return self._player_that_human is not None

    @property
    def player_that_human(self) -> str:
        """
        Retrieves the final result of the evaluation.

        Returns:
            str: The result string.

        Raises:
            ResultIsNotReadyError: If the result is not yet available.

        """
        if self._player_that_human is None:
            raise ResultIsNotReadyError

        return self._player_that_human
