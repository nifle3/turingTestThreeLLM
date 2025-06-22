from os import getenv
import json
from typing import Any
from logging import getLogger, Logger

from system_prompts import SystemPrompts
from model_metadata import ModelMetadata


logger: Logger = getLogger(__name__)


def _main() -> None:
    if getenv("APP_ENV", "DEVELOPMENT") == "DEVELOPMENT":
        from dotenv import load_dotenv
        load_dotenv()

    with open("system_prompts.json", "r") as file:
        data: Any = json.load(file)

    system_prompts: SystemPrompts = SystemPrompts(**data)

    with open("model_metadata.json", "r") as file:
        model_metadata_json: list[Any] = json.load(file)

    model_metadatas: list[ModelMetadata] = []

    for i in model_metadata_json:
        model_metadatas.append(ModelMetadata(**i))

    logger.debug(t"system_prompts: {system_prompts}")
    print(f"model_metadats {model_metadatas}")

if __name__ == "__main__":
    _main()
