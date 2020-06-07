from RingingBot import RingingBot
from RowGeneration.ComplibCompositionReader import ComplibCompositionReader
from RowGeneration.DixonoidsGenerator import DixonoidsGenerator
from RowGeneration.MethodPlaceNotationGenerator import MethodPlaceNotationGenerator
from RowGeneration.PlainHuntGenerator import PlainHuntGenerator
from RowGeneration.PlaceNotationGenerator import PlaceNotationGenerator
from RingingRoomTower import RingingRoomTower

DEFAULT_URL = "http://localhost:8080"
INTERBELL_GAP = 0.2

TOWER_ID = 495826713


def null_log(string):
    pass


def main():
    tower = RingingRoomTower(TOWER_ID, DEFAULT_URL)

    # row_gen = PlainHuntGenerator(8)
    row_gen = PlaceNotationGenerator(8, "x1", bob={1: "6"})
    # row_gen = ComplibCompositionReader(65034)
    # row_gen = MethodPlaceNotationGenerator("Single Oxford Bob Triples")
    # row_gen = DixonoidsGenerator(6, DixonoidsGenerator.DixonsRules)
    # row_gen = PlaceNotationGenerator.stedman(11)

    bot = RingingBot(tower, row_gen, INTERBELL_GAP, auto_start=True)

    bot.main_loop(initialise_tower=True)


if __name__ == '__main__':
    main()
