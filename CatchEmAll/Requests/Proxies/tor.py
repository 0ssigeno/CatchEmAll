from stem import Signal
from stem.control import Controller

from CatchEmAll.Requests.proxy import Proxy


class Tor(Proxy):

    def remove_proxy(self):
        pass

    def __init__(self, passphrase: str, controller_port: int = 9051,
                 socks_port: int = 9050):
        if passphrase is None:
            raise Exception("Please insert your tor passphrase")
        super().__init__("tor")
        self.passphrase = passphrase
        self.port = port
        self.controller = Controller.from_port(port=controller_port)
        self.controller.authenticate(self.passphrase)

    def _get_random_server(self, usr, pwd, nation=None):
        self.controller.signal(Signal.NEWNYM)
        return "socks5h://localhost:" + str(self.port)
