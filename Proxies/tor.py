import getpass

from stem import Signal
from stem.control import Controller

from config import read_tor, write_tor


class Tor:

    def __init__(self):
        try:
            self.passphrase = read_tor()
        except KeyError:
            self.passphrase = getpass.getpass("Please insert your node controller passphrase\n")
            write_tor(self.passphrase)
        self.controller = Controller.from_port(port=9051)
        self.controller.authenticate(self.passphrase)


    def get_random_server(self):
        # TODO i dont how this shit work with multithread, probably they will steal each other the IP
        self.controller.signal(Signal.NEWNYM)
        return "socks5h://localhost:9050"
