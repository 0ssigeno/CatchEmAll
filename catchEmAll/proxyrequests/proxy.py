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

    def get_server(self, usr: str = "", pwd: str = "", nation=None) -> str:
        self.usr = usr
        self.pwd = pwd
        self.server = self._get_random_server(usr, pwd, nation)
        logging.debug("PROXY: server changed to %s".format(self.server))
        return self.server
