from dataclasses import dataclass
from typing import final


@dataclass
@final
class SystemPrompts:

    judge: str
    human: str
    computer: str
