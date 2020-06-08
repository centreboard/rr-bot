import logging
from time import sleep

from Calls import Calls
from RingingRoomTower import RingingRoomTower
from RowGeneration.RowGenerator import RowGenerator


class RingingBot:
    logger_name = "BOT"

    def __init__(self, tower: RingingRoomTower, row_gen: RowGenerator, bell_gap: float, auto_start=True):
        self.tower = tower
        self.row_gen = row_gen
        self.bell_gap = bell_gap
        self.auto_start = auto_start
        self.logger = logging.getLogger(self.logger_name)

        self.should_ring = False
        self.should_stand = False

        self.is_handstroke = True

        tower.on_call = self.process_call
        tower.on_reset = self._process_reset

    def main_loop(self, initialise_tower: bool):
        with self.tower:
            if initialise_tower:
                self._initialise_tower()

            while True:
                self.tower.wait_loaded()

                if self.auto_start and not self.tower.user_controlled(1):
                    self.tower.make_call(Calls.LookTo)
                    self.should_ring = True
                    sleep(3)
                if not self.should_ring or self.should_stand:
                    sleep(self.bell_gap)
                    continue
                self.ring()

    def ring(self):
        self.logger.info("Start Ringing")
        while not self.should_stand or not self.is_handstroke:
            row = self.row_gen.next_row(self.is_handstroke)
            self.ring_row(row)
            if not self.is_handstroke:
                self.logger.debug("Handstroke gap")
                sleep(self.bell_gap)
            self.is_handstroke = not self.is_handstroke
        self.row_gen.reset()
        self.logger.info("Stopped Ringing")

    def ring_row(self, row: []):
        for bell in row:
            if not self.tower.user_controlled(bell):
                self.logger.debug(f"User controlled {bell}")
                self.tower.ring_bell(bell, self.is_handstroke)
            sleep(self.bell_gap)

    def process_call(self, call: str):
        self.logger.info(f"Processing call '{call}'")
        if call == Calls.LookTo:
            sleep(3)
            self.should_ring = True
            self.should_stand = False
        elif call == Calls.Stand:
            self.auto_start = False
            self.should_stand = True
        elif call == Calls.Go:
            self.row_gen.go()
        elif call == Calls.Bob:
            self.row_gen.bob()
        elif call == Calls.Single:
            self.row_gen.single()
        elif call == Calls.ThatsAll:
            self.row_gen.reset()
        else:
            self.logger.warning(f"Unhandled call '{call}'")

    def _process_reset(self):
        self.logger.info("Reset")
        self.should_ring = False

    def _initialise_tower(self):
        self.logger.info("Initialise Tower")
        self.tower.set_number_of_bells(self.row_gen.number_of_bells)
        self.tower.set_at_hand()
