from stem import Signal
from stem.control import Controller

from catchEmAll.proxyrequests.proxy import Proxy


# FIXME come gestisco multithread e tor?


class Tor(Proxy):

    def remove_proxy(self):
        pass

    def __init__(self, passphrase: str, controller_port: int = 9051, socks_port: int = 9050):
        if passphrase is None:
            raise ValueError("Please insert your tor passphrase")
        super().__init__("tor")
        self.passphrase = passphrase
        self.port = socks_port
        self.controller = Controller.from_port(port=controller_port)
        self.controller.authenticate(self.passphrase)

    def _get_random_server(self, usr, pwd, nation=None):
        self.controller.signal(Signal.NEWNYM)
        return "socks5h://localhost:" + str(self.port)
