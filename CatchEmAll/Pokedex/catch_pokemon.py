import random
from multiprocessing import Process

from CatchEmAll.Pokedex.pokeball import Pokeball
from CatchEmAll.utils import *


class CatchPokemon:

    def __init__(self, db_usr: str, db_pwd: str, db_host: str, db_db: str, max_threads: int = 2):
        self._max_threads = max_threads
        self._db_usr, self._db_pwd, self._db_host, self._db_db = db_usr, db_pwd, db_host, db_db

    def _catch(self, functions: []):
        random.shuffle(functions)
        pokeball = Pokeball(self._db_usr, self._db_pwd, self._db_host, self._db_db)
        while pokeball.find_user([func.__name__ for func in functions]):
            func = nameToFunc(pokeball.site, functions)
            result = func(pokeball.get_proxy(), pokeball.usr, pokeball.pwd)
            pokeball.save(result)
            pokeball.hide()
        else:
            return

    def catchEmAll(self, functions: [], timeout: int = 10):
        processes = []
        for i in range(self._max_threads):
            p = Process(target=self._catch, args=(functions,))
            processes.append(p)
            p.start()
        for i in range(self._max_threads):
            processes[i].join(timeout=timeout)
