from dataclasses import dataclass
from typing import final

@dataclass
@final
class ModelMetadata:

    provider: str
    name: str

    def __str__(self) -> str:
        return f"{self.provider} - {self.name}"
