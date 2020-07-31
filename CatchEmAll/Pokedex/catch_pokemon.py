import random
from multiprocessing import Process

from CatchEmAll.Pokedex.pokeball import Pokeball
from CatchEmAll.utils import *


class CatchPokemon:

    def __init__(self, db_usr: str, db_pwd: str, db_host: str, db_db: str, max_threads: int = 2):
        self._max_threads = max_threads
        self._db_usr, self._db_pwd, self._db_host, self._db_db = db_usr, db_pwd, db_host, db_db

    def _catch(self, functions: []):
        pokeball = Pokeball(self._db_usr, self._db_pwd, self._db_host, self._db_db)
        if self.tor:
            pokeball.allow_tor(self.tor_password)
        pokeball.hide(force=True)
        funcs_names = [func.__name__ for func in functions]
        while pokeball.find_user(funcs_names):
            func = nameToFunc(pokeball.site, functions)
            pokeball.catch(func)
            random.shuffle(funcs_names)
        else:
            return

    def catchEmAll(self, functions: [], tor: bool = False, tor_password: str = None, timeout: int = 10):
        self.tor = tor
        self.tor_password = tor_password
        self.processes = []
        for i in range(self._max_threads):
            p = Process(target=self._catch, args=(functions,))
            self.processes.append(p)
            p.start()
        for i in range(self._max_threads):
            self.processes[i].join(timeout=timeout)
