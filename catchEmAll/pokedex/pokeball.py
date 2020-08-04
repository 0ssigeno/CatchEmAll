import logging as log
import random

from fake_useragent import UserAgent

from catchEmAll.database.db_manager import DbManager
from catchEmAll.proxyrequests.proxies import *


class Pokeball:

    def __init__(self, dbm: DbManager, tor: Tor = None):
        self.providers = [NordVpn()]
        self._tor = tor
        self._dbm = dbm
        self._ua = UserAgent()
        self._proxy_obj = None

        self._usr = None
        self._pwd = None
        self._site = None
        self.request_proxy = {}

    def catch(self, function):
        res = function(self)
        self._save(res)
        self._change_proxy()

    def find_user_to_test(self, columns: []) -> bool:
        for column in columns:
            res = self._dbm.retrieve_users(column, None)
            if res:
                self._usr, self._pwd = random.choice(res)
                self._site = column
                return True
        return False

    def get_account(self) -> (str, str):
        return self._usr, self._pwd

    def _change_proxy(self, country="Italy", force: bool = False):
        random.shuffle(self.providers)
        for provider in self.providers:
            provider_name = provider.__class__.__name__.lower()
            users = self._dbm.retrieve_users(provider_name, True)
            if users:
                usr, pwd = random.choice(users)
                self._proxy_obj = provider
                self.request_proxy = self._proxy_obj.get_server(usr, pwd, country, force=force)
            else:
                log.warning("No users available for {}".format(provider_name))
                self._dbm.add_column(provider_name)
        if self._tor is not None:
            self._proxy_obj = self._tor
            self.request_proxy = self._proxy_obj.get_server()
        else:
            self._proxy_obj = None
            self.request_proxy = {}

    def _remove_proxy(self, e: Exception):
        if self._proxy_obj:
            if e == ProxyError:
                log.warning("Proxy {} {} not valid".format(self._proxy_obj.usr, self._proxy_obj.pwd))
                self._dbm.update_result(self._proxy_obj.usr, self._proxy_obj.pwd, False, self._proxy_obj.provider)
            # server do not work
            elif e == ConnectTimeout:
                log.warning("Removing proxy {}".format(self._proxy_obj.server))
                self._proxy_obj.remove_server()
            else:
                raise NotImplementedError("Error not implemented")
        else:
            # todo
            pass
        self._change_proxy(force=True)

    def requests_function(self, func, url, **kwargs):
        # TODO session object
        """
        To use inside the pokedex functions
        """

        if "headers" not in kwargs:
            kwargs["headers"] = {}
        if "User-Agent" not in kwargs["headers"]:
            kwargs["headers"]["User-Agent"] = self._ua.random
        kwargs["proxies"] = self.request_proxy
        data = kwargs.pop("data") if "data" in kwargs else None
        json = kwargs.pop("json") if "json" in kwargs else None
        params = kwargs.pop("params") if "params" in kwargs else None

        try:
            return func(url, data=data, json=json, params=params ** kwargs)
        except Exception as e:
            self._remove_proxy(e)
            return self.requests_function(func, **kwargs)

    def _save(self, result: bool):
        self._dbm.update_result(self._usr, self._pwd, result, self._site)
        log.debug("Account valid {}:{} on site {} ".format(self._usr, self._pwd, self._site)) if result else \
            log.info("Account error {}:{} on site {} ".format(self._usr, self._pwd, self._site))
