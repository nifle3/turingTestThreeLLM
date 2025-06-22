from dataclasses import dataclass

@dataclass
class ModelMetadata:

    provider: str
    name: str

    def __str__(self) -> str:
        return f"{self.provider} - {self.name}"
