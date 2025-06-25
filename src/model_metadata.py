from dataclasses import dataclass
from typing import final


@dataclass
@final
class ModelMetadata:
    """
    Dataclass representing metadata for a language model, typically loaded from a JSON file.

    Attributes:
        provider (str): The provider or vendor of the model (e.g., OpenAI, Anthropic).
        name (str): The specific name or identifier of the model (e.g., gpt-4, claude-3).

    """

    provider: str
    name: str

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the model metadata.

        Returns:
            str: A string in the format "<provider> - <name>".

        """
        return f"{self.provider} - {self.name}"
