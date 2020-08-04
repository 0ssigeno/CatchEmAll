import importlib
import logging

from catchEmAll.database.db_manager import DbManager
from catchEmAll.pokedex.catch_pokemon import CatchPokemon


class Ash:
    format_log = "%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s"

    def __init__(self, max_threads: int = 2, max_req_same_proxy: int = 5,
                 pokedex_path: str = "catchEmAll.pokedex.captured"):
        logging.basicConfig(format=self.format_log)
        self._max_threads = max_threads
        self._max_req_proxy = max_req_same_proxy
        self._pokedex_path = pokedex_path
        self._pokemons = self._import_pokedex()
        self.log_level = logging.WARNING
        logging.debug("Ash creation complete")

    def _import_pokedex(self) -> list:
        module = importlib.import_module(self._pokedex_path)

        functions_to_executes = [getattr(module, func) for func in dir(module) if not func.startswith("_")]
        return functions_to_executes

    def ail_populate_db(self, path: str):
        self._dbm.populate_db(path)

    def init(self, usr: str, pwd: str, host: str, db: str):
        self._dbm = DbManager(usr, pwd, host, db)
        self._dbm.initialize()
        for func in self._pokemons:
            self._dbm.add_column(func.__name__)
        self._cp = CatchPokemon(self._dbm)

    def start(self, timeout=10):
        self._cp.catchEmAll(self._pokemons, timeout=timeout)
