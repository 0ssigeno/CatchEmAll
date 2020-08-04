import logging
from abc import abstractmethod
from multiprocessing import Lock


class Proxy:
    def __init__(self, name: str):
        self.provider = name
        self.max_counter = 3  # todo attributo
        self.counter = self.max_counter
        self.mutex = Lock()
        self.usr = None
        self.pwd = None
        self.server = None

    @abstractmethod
    def _get_random_server(self, usr: str, pwd: str, nation=None) -> str:
        pass

    @abstractmethod
    def remove_server(self):
        pass

    def get_server(self, usr: str = "", pwd: str = "", nation=None, force: bool = False) -> dict:
        self.mutex.acquire()
        if self.counter == self.max_counter or force:
            self.counter = 0
            self.mutex.release()
            self.usr = usr
            self.pwd = pwd
            self.server = self._get_random_server(usr, pwd, nation)
            logging.debug("PROXY: server changed to %s".format(self.server))
            return {"https": self.server}
        self.counter += 1
        self.mutex.release()

        return {"https": self.server}
