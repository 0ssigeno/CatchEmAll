import logging as log
import random

from CatchEmAll.Database.db_manager import DbManager
from CatchEmAll.Requests.proxy_requests import ProxyRequest


class Pokeball:

    def __init__(self, usr: str, pwd: str, host: str, db: str):
        self._dbm = DbManager(usr, pwd, host, db)
        self._dbm.login()
        self.pr = ProxyRequest(self._dbm)

    def allow_tor(self, tor_passphrase: str):
        self.pr.allow_tor(tor_passphrase)

    def hide(self, force=False):
        self.pr.hide(force=force)

    def catch(self, function):
        res = function(self.usr, self.pwd, self.pr)
        self.save(res)
        self.hide()

    def find_user(self, columns: []) -> bool:
        for column in columns:
            res = self._dbm.retrieve_users(column, None)
            if res:
                self.usr, self.pwd = random.choice(res)
                self.site = column
                return True
        return False

    def save(self, result: bool):
        self._dbm.update_result(self.usr, self.pwd, result, self.site)
        log.debug("Account valid {}:{} on site {} ".format(self.usr, self.pwd, self.site)) if result else \
            log.info("Account error {}:{} on site {} ".format(self.usr, self.pwd, self.site))
