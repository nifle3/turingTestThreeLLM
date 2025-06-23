from os import getenv
import json
from typing import Any, Tuple
import logging
from random import randrange

from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel

from judge import Judge, LangChainJudge
from player import Player, LangChainPlayer
from game import Game
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
    judge: ModelMetadata = asker_with_retry(user_asker, "Введите модель судьи")
    human: ModelMetadata = asker_with_retry(user_asker, "Введите модель человека")
    computer: ModelMetadata = asker_with_retry(user_asker, "Введите модель компьютера")

    logger.debug("selected judge - %s", judge)
    logger.debug("selected human - %s", human)
    logger.debug("selected computer - %s", computer)

    judge_model: BaseChatModel = init_chat_model(judge.name, model_provider=judge.provider)
    human_model: BaseChatModel = init_chat_model(human.name, model_provider=human.provider)
    computer_model: BaseChatModel = init_chat_model(computer.name, model_provider=computer.provider)

    judge_player = LangChainJudge(judge_model)
    human_player = LangChainPlayer(human_model)
    computer_player = LangChainPlayer(computer_model)

def asker_with_retry(asker: UserAsker, title: str) -> ModelMetadata:
    asker.print(title)
    while True:
        try:
            return asker.input()
        except InvalidInputIndexError:
           print("Модели с таким индексом нет")
        except InvalidInputTypeError:
           print("Вы должны ввести число")

def create_game(judge: Judge, first_player: Player, second_player: Player) -> Game:
    rand = randrange(0, 100)
    if rand % 2 == 0:
        players: Tuple[Player, Player] = (first_player, second_player)
    else:
        players: Tuple[Player, Player] = (second_player, first_player)

    return Game(
        players = players,
        judge = judge
    )

if __name__ == "__main__":
    _main()
