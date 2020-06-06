from RingingBot import RingingBot
from RowGenerator import PlainHuntGenerator
from Tower import Tower

DEFAULT_URL = "http://localhost:8080"
INTERBELL_GAP = 0.2

TOWER_ID = 495826713


def main():
    tower = Tower(TOWER_ID, DEFAULT_URL)
    row_gen = PlainHuntGenerator(8)
    ringing = RingingBot(tower, row_gen, INTERBELL_GAP, True)

    ringing.initialise_tower()
    ringing.main_loop()


if __name__ == '__main__':
    main()
