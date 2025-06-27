import json
import logging
from os import getenv
from pathlib import Path
from secrets import randbelow
from typing import Any

from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel
from rich.console import Console

from model_metadata import ModelMetadata
from models.judge import Judge, LangChainJudge
from models.player import LangChainPlayer, Player
from system_prompts import SystemPrompts
from turing_test import TuringTest, TuringTestForTwoPlayer
from user_asker import DefaultUserAsker
from printer import RichPrinter


def _main() -> None:
    """
    Main entry point of the application.

    Loads configuration and model metadata from JSON files,
    initializes logging, prompts the user to select models for
    judge, human, and computer players, initializes LangChain models,
    creates the Turing test game, and starts the game.
    """
    if getenv("APP_ENV", "DEVELOPMENT").upper() == "DEVELOPMENT":
        from dotenv import load_dotenv
        load_dotenv()

    logging.basicConfig(level=getenv("LOGGER_LEVEL", "debug").upper())
    logger: logging.Logger = logging.getLogger(__name__)

    system_prompts_file = Path("system_prompts.json")
    with system_prompts_file.open(encoding="UTF-8") as prompt_file:
        prompt_data: Any = json.load(prompt_file)

    system_prompts: SystemPrompts = SystemPrompts(**prompt_data)

    model_metadata_file = Path("model_metadata.json")
    with model_metadata_file.open(encoding="UTF-8") as model_metadata_file:
        model_metadata_json: list[Any] = json.load(prompt_data)

    model_metadatas = [ModelMetadata(**metadata) for metadata in model_metadata_json]

    logger.debug("system_prompts: %s", system_prompts)
    logger.debug("model_metadatas: %s", model_metadatas)

    user_asker = DefaultUserAsker(model_metadatas, Console())
    judge: ModelMetadata = user_asker.ask("Введите модель судьи")
    human: ModelMetadata = user_asker.ask("Введите модель человека")
    computer: ModelMetadata = user_asker.ask("Введите модель компьютера")

    logger.debug("selected judge - %s", judge)
    logger.debug("selected human - %s", human)
    logger.debug("selected computer - %s", computer)

    judge_model: BaseChatModel = init_chat_model(judge.name, model_provider=judge.provider)
    human_model: BaseChatModel = init_chat_model(human.name, model_provider=human.provider)
    computer_model: BaseChatModel = init_chat_model(computer.name, model_provider=computer.provider)

    judge_player = LangChainJudge(judge_model, system_prompts.judge)
    human_player = LangChainPlayer(human_model, system_prompts.human)
    computer_player = LangChainPlayer(computer_model, system_prompts.computer)

    printer = RichPrinter(Console())

    game = create_game(judge_player, human_player, computer_player)
    generator = game.start()

    printer.start_output(generator)

def create_game(judge: Judge, first_player: Player, second_player: Player) -> TuringTest:
    """
    Creates a TuringTestForTwoPlayer game with players arranged in random order.

    Args:
        judge (Judge): The judge instance that evaluates the game.
        first_player (Player): The first player instance.
        second_player (Player): The second player instance.

    Returns:
        TuringTest: An instance of TuringTestForTwoPlayer with randomized player order.

    """
    rand = randbelow(100)
    if rand % 2 == 0:
        players: tuple[Player, Player] = (first_player, second_player)
    else:
        players: tuple[Player, Player] = (second_player, first_player)

    return TuringTestForTwoPlayer(
        players=players,
        judge=judge
    )


if __name__ == "__main__":
    _main()
