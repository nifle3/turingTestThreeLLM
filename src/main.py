from os import getenv
import json
from typing import Any
import logging

from system_prompts import SystemPrompts
from model_metadata import ModelMetadata
from user_asker import UserAsker, DefaultUserAsker, InvalidInputIndexError, InvalidInputTypeError

def _main() -> None:
    if getenv("APP_ENV", "DEVELOPMENT").upper() == "DEVELOPMENT":
        from dotenv import load_dotenv
        load_dotenv()

    logging.basicConfig(level=getenv("LOGGER_LEVEL", "debug").upper())
    logger: logging.Logger = logging.getLogger(__name__)

    with open("system_prompts.json", "r") as file:
        data: Any = json.load(file)

    system_prompts: SystemPrompts = SystemPrompts(**data)

    with open("model_metadata.json", "r") as file:
        model_metadata_json: list[Any] = json.load(file)

    model_metadatas: list[ModelMetadata] = []

    for i in model_metadata_json:
        model_metadatas.append(ModelMetadata(**i))

    logger.debug("system_prompts: %s", system_prompts)
    logger.debug("model_metadatas: %s", model_metadatas)

    user_asker = DefaultUserAsker(model_metadatas)
    judge = asker_with_retry(user_asker, "Введите модель судьи")
    human = asker_with_retry(user_asker, "Введите модель человека")
    computer = asker_with_retry(user_asker, "Введите модель компьютера")

    logger.debug("selected judge - %s", judge)
    logger.debug("selected human - %s", human)
    logger.debug("selected computer - %s", computer)

def asker_with_retry(asker: UserAsker, title: str) -> ModelMetadata:
    asker.print(title)
    while True:
        try:
            return asker.input()
        except InvalidInputIndexError:
           print("Модели с таким индексом нет")
        except InvalidInputTypeError:
           print("Вы должны ввести число")

if __name__ == "__main__":
    _main()
