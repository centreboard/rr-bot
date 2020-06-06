from time import sleep

import socketio


class Tower:
    def __init__(self, tower_id: int, url: str, log_bells=False, logger=print):
        self.tower_id = tower_id
        self.logger = logger
        self._log_bells = log_bells
        self._bell_state = []
        self._assigned_users = {}

        self.on_call = None
        self.on_reset = None

        self._socket_io_client = self._create_client(url)

    @property
    def number_of_bells(self):
        return len(self._bell_state)

    def wait_loaded(self):
        while not self._bell_state:
            sleep(0.1)

    def ring_bell(self, bell: int, handstroke: bool):
        try:
            if bell > len(self._bell_state) or bell <= 0:
                self.log_error(f"Bell {bell} not in tower")
                return False
            stroke = self._bell_state[bell - 1]
            if stroke != handstroke:
                self.log_error(f"Bell {bell} on opposite stroke")
                return False
            self._socket_io_client.emit("c_bell_rung", {"bell": bell, "stroke": stroke, "tower_id": self.tower_id})
            return True
        except Exception as e:
            self.logger(e)
            return False

    def user_controlled(self, bell: int):
        return self._assigned_users.get(bell, "") != ""

    def make_call(self, call: str):
        self.log_emit(f"Call '{call}'")
        self._socket_io_client.emit("c_call", {"call": call, "tower_id": self.tower_id})

    def set_at_hand(self):
        self.log_emit(f"Set at hand")
        self._socket_io_client.emit("c_set_bells", {"tower_id": self.tower_id})

    def set_number_of_bells(self, number: int):
        self.log_emit(f"Set number of bells '{number}'")
        self._socket_io_client.emit("c_size_change", {"new_size": number, "tower_id": self.tower_id})

    def _create_client(self, url):
        sio = socketio.Client()
        sio.connect(url)
        # Currently just care about global state when a bell in rung
        sio.on("s_bell_rung", self._on_global_bell_state)
        sio.on("s_global_state", self._on_global_bell_state)
        sio.on("s_size_change", self._on_size_change)
        sio.on("s_assign_user", self._on_assign_user)
        sio.on("s_call", self._on_call)

        sio.emit("c_join", {"anonymous_user": True, "tower_id": self.tower_id})
        sio.emit('c_request_global_state', {"tower_id": self.tower_id})

        return sio

    def _on_global_bell_state(self, data):
        bell_state = data["global_bell_state"]
        self._bell_state = bell_state
        if self._log_bells:
            self.log_received(f"Bells '{['H' if x else 'B' for x in bell_state]}'")

    def _on_size_change(self, data):
        new_size = data["size"]
        if new_size != self.number_of_bells:
            self._assigned_users = {}
            self._bell_state = self._bells_set_at_hand(new_size)
            self.log_received(f"New tower size '{new_size}'")
            if self.on_reset is not None:
                self.on_reset()

    def _on_assign_user(self, data):
        bell = data["bell"]
        user = data["user"]
        self._assigned_users[bell] = user
        self.log_received(f"Assigned bell '{bell}' to '{user or 'BOT'}'")

    def _on_call(self, data):
        call = data["call"]
        self.log_received(f"Call '{call}'")
        if self.on_call is not None:
            self.on_call(call)

    @staticmethod
    def _bells_set_at_hand(number: int):
        return [True for _ in range(number)]

    def log_error(self, message: str):
        self.logger(f"ERROR: {message}")

    def log_emit(self, message: str):
        self.logger(f"EMIT: {message}")

    def log_received(self, message: str):
        self.logger(f"RECEIVED: {message}")
