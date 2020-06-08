import logging
import sys

from RingingBot import RingingBot
from RowGeneration.ComplibCompositionReader import ComplibCompositionReader
from RowGeneration.GoAndStopCallingGenerator import GoAndStopCallingGenerator
from RowGeneration.DixonoidsGenerator import DixonoidsGenerator
from RowGeneration.MethodPlaceNotationGenerator import MethodPlaceNotationGenerator
from RowGeneration.PlainHuntGenerator import PlainHuntGenerator
from RowGeneration.PlaceNotationGenerator import PlaceNotationGenerator
from RingingRoomTower import RingingRoomTower
from RowGeneration.RowGenerator import RowGenerator

DEFAULT_URL = "http://localhost:8080"
INTERBELL_GAP = 0.2

TOWER_ID = 495826713


def null_log(string):
    pass


def row_generator():
    # row_gen = PlainHuntGenerator(8)
    row_gen = PlaceNotationGenerator(8, "x1", bob={1: "6"})
    # row_gen = ComplibCompositionReader(65034)
    # row_gen = MethodPlaceNotationGenerator("Single Oxford Bob Triples")
    # row_gen = DixonoidsGenerator(6, DixonoidsGenerator.DixonsRules)
    # row_gen = PlaceNotationGenerator.stedman(11)
    return row_gen


def configure_logging():
    logging.basicConfig(level=logging.WARNING)

    logging.getLogger(RingingRoomTower.logger_name).setLevel(logging.INFO)
    logging.getLogger(RingingBot.logger_name).setLevel(logging.INFO)
    logging.getLogger(RowGenerator.logger_name).setLevel(logging.INFO)


def main():
    configure_logging()

    tower = RingingRoomTower(TOWER_ID, DEFAULT_URL)

    row_gen = row_generator()

    bot = RingingBot(tower, row_gen, INTERBELL_GAP, call_look_to=True)

    bot.main_loop(initialise_tower=True)


if __name__ == '__main__':
    main()
