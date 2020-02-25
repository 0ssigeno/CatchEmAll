from stem import Signal
from stem.control import Controller


class Tor:

    def __init__(self):
        self.passphrase = ""
        self.controller = Controller.from_port(port=9051)
        self.controller.authenticate(self.passphrase)

    def _load_pwd(self):
        pass

    def get_random_server(self):
        self.controller.signal(Signal.NEWNYM)
        return "socks5h://localhost:9050"
