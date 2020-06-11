import logging
from time import sleep

from Calls import Calls
from RingingRoomTower import RingingRoomTower
from RowGeneration.RowGenerator import RowGenerator

class BellGap:
    def __init__(self, target: float):
        self.target = target
        self.gap = target

    def wait(self):
        sleep(self.gap)


class RingingBot:
    logger_name = "BOT"

    def __init__(self, tower: RingingRoomTower, row_gen: RowGenerator, bell_gap: float,
                 call_look_to=True, stop_at_rounds=True, call_thats_all=False, wait_for_user=False):
        self.tower = tower
        self.row_gen = row_gen
        self.bell_gap = bell_gap
        self.wait_for_user = wait_for_user

        self.call_look_to = call_look_to
        self.stop_at_rounds = stop_at_rounds
        self.call_thats_all = call_thats_all

        self.logger = logging.getLogger(self.logger_name)

        self.should_ring = False
        self.should_stand = False

        self.is_handstroke = True
        self._has_gone = False

        tower.on_call = self.process_call
        tower.on_reset = self.reset

    def main_loop(self, initialise_tower: bool):
        with self.tower:
            if initialise_tower:
                self._initialise_tower()

            while True:
                self.tower.wait_loaded()

                if self.call_look_to and not self.tower.user_controlled(1):
                    self.call_look_to = False
                    self.make_call(Calls.LookTo)
                    self.should_ring = True
                    sleep(3)
                if not self.should_ring or self.should_stand:
                    sleep(self.bell_gap)
                    continue
                self.ring()

    def ring(self):
        self.logger.info("Start Ringing")
        rounds = self.row_gen.rounds()

        while self.should_ring and (not self.should_stand or not self.is_handstroke):
            row = self.row_gen.next_row(self.is_handstroke)

            self._set_stopping_if_rounds(rounds, row)

            self.ring_row(row)
            if not self.is_handstroke:
                self.logger.debug("Handstroke gap")
                sleep(self.bell_gap)
            self.is_handstroke = not self.is_handstroke

        self.reset()
        self.logger.info("Stopped Ringing")

    def ring_row(self, row: []):
        for bell in row:
            if not self.should_ring:
                self.logger.warning("Stopping")
                return
            if not self.tower.user_controlled(bell):
                self.logger.debug(f"User controlled {bell}")
                self.tower.ring_bell(bell, self.is_handstroke)
            elif self.wait_for_user:
                while not self.tower.has_bell_rung(bell, self.is_handstroke):
                    sleep(0.01)
            sleep(self.bell_gap)

    def _set_stopping_if_rounds(self, rounds, row):
        if self._has_gone and row == rounds and self.stop_at_rounds:
            self._has_gone = False
            self.should_stand = True
            if self.call_thats_all:
                self.make_call(Calls.ThatsAll)
        elif row != rounds:
            self._has_gone = True

    def make_call(self, call: str):
        self.logger.info(f"Make Call '{call}'")
        self.tower.make_call(call)

    def process_call(self, call: str):
        self.logger.info(f"Processing Call '{call}'")
        if call == Calls.LookTo:
            sleep(3)
            self.should_ring = True
            self.should_stand = False
        elif call == Calls.Stand:
            self.call_look_to = False
            self.should_stand = True
        elif call == Calls.Go:
            self.row_gen.set_go()
        elif call == Calls.Bob:
            self.row_gen.set_bob()
        elif call == Calls.Single:
            self.row_gen.set_single()
        elif call == Calls.ThatsAll:
            self.row_gen.reset()
        else:
            self.logger.error(f"Unhandled call '{call}'")

    def reset(self):
        self.logger.info("Reset")
        self.should_ring = False
        self.should_stand = False

        self.is_handstroke = True
        self._has_gone = False

        self.row_gen.reset()

    def _initialise_tower(self):
        self.logger.info("Initialise Tower")
        self.tower.set_number_of_bells(self.row_gen.number_of_bells)
        self.tower.set_at_hand()
