from dataclasses import dataclass

@dataclass
class SystemPrompts:

    judge: str
    human: str
    computer: str
