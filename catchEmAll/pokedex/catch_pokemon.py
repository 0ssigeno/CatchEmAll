import random
from multiprocessing import Process

from catchEmAll.database.db_manager import DbManager
from catchEmAll.pokedex.pokeball import Pokeball
from catchEmAll.proxyrequests.proxies.tor import Tor
from catchEmAll.utils import *


class CatchPokemon:

    def __init__(self, dbm: DbManager, max_threads: int = 2):
        self._max_threads = max_threads
        self.tor = None
        self.processes = []
        self.dbm = dbm

    def _catch(self, i: int, functions: []):
        pokeball = Pokeball(self.dbm, self.tor)
        funcs_names = [func.__name__ for func in functions]
        while pokeball.find_user_to_test(funcs_names):
            func = nameToFunc(pokeball._site, functions)
            pokeball.catch(func)
            random.shuffle(funcs_names)
        else:
            return

    def allow_tor(self, tor_passphrase: str):
        self.tor = Tor(tor_passphrase)

    def catchEmAll(self, functions: [], timeout: int = 10):
        for i in range(self._max_threads):
            p = Process(target=self._catch, args=(i, functions))
            self.processes.append(p)
            p.start()
        for i in range(self._max_threads):
            self.processes[i].join(timeout=timeout)
