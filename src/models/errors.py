from typing import final


@final
class InvalidOutputLLMError(Exception):
    """Exception raised when the output from the language model is not str."""
