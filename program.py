from RingingBot import RingingBot
from RowGeneration.ComplibCompositionReader import ComplibCompositionReader
from RowGeneration.MethodPlaceNotationGenerator import MethodPlaceNotationGenerator
from RowGeneration.PlainHuntGenerator import PlainHuntGenerator
from RowGeneration.PlaceNotationGenerator import PlaceNotationGenerator
from Tower import Tower

DEFAULT_URL = "http://localhost:8080"
INTERBELL_GAP = 0.2

TOWER_ID = 495826713


def null_log(string):
    pass


def main():
    tower = Tower(TOWER_ID, DEFAULT_URL)
    # row_gen = PlainHuntGenerator(8)
    # row_gen = PlaceNotationGenerator(8, "&x1x1x1x1", "2")
    # row_gen = ComplibCompositionReader(65034)
    row_gen = MethodPlaceNotationGenerator("Cambridge Surprise Minor")
    bot = RingingBot(tower, row_gen, INTERBELL_GAP, auto_start=True)

    bot.initialise_tower()
    bot.main_loop()


if __name__ == '__main__':
    main()
