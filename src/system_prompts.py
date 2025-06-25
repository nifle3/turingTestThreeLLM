from dataclasses import dataclass
from typing import final


@dataclass
@final
class SystemPrompts:
    """Data class represent json format of system prompts.json."""

    judge: str
    human: str
    computer: str
