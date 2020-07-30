import logging
from abc import abstractmethod


class Proxy:
    def __init__(self, name: str):
        self.provider = name

    @abstractmethod
    def _get_random_server(self, usr: str, pwd: str, nation=None) -> str:
        pass

    @abstractmethod
    def remove_proxy(self):
        pass

    def server(self, usr: str = "", pwd: str = "", nation=None) -> str:
        self.usr = usr
        self.pwd = pwd
        self._server = self._get_random_server(usr, pwd, nation)
        logging.debug("PROXY: server changed to %s".format(self._server))
        return self._server
