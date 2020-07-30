import logging as log
import random

import requests
from fake_useragent import UserAgent
from mysql.connector.errors import ProgrammingError
from requests.exceptions import ProxyError, ConnectTimeout

from CatchEmAll.Database.db_manager import DbManager
from CatchEmAll.Requests.Proxies import *


class ProxyRequest:
    proxy_providers = ["nordvpn"]

    def __init__(self, db: DbManager, max_requests_before_change: int = 5, allowTor: bool = False,
                 tor_passphrase: str = None,
                 *args, **kwargs):
        # super().__init__(*args, **kwargs)
        self._db = db
        self._tor_passphrase = tor_passphrase
        self._max_req = max_requests_before_change
        self._canUseTor = allowTor
        self._ua_obj = UserAgent()
        self._counter = 0
        self._proxy = None
        log.debug("Init PR done")

    def get(self, url: str, params=None, **kwargs):
        kwargs["params"] = params
        return self._proxy_wrapper(url, "get", 0, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        kwargs["data"] = data
        kwargs["json"] = json
        return self._proxy_wrapper(url, "get", 0, **kwargs)

    def hide(self, force=False, nation=None):
        if self._counter == self._max_req or force:
            self._counter = 0
            self._set_random_user_agent()
            self._use_proxy(random.choice(self.proxy_providers), nation)
            log.debug("PR: Changing proxy")
        self._counter += 1

    def _set_proxy(self, proxy: str):
        self.proxies = {"https": proxy}

    def _use_proxy(self, provider, nation=None):
        try:
            users = self._db.retrieve_users(provider, True)
        except ProgrammingError:
            log.warning("You don't have a {} column".format(provider))
            self._db.add_column(provider)
            self._try_tor()
            return
        if users:
            usr, pwd = random.choice(users)
        else:
            log.warning("No users available for {}".format(provider))
            self._try_tor()
            return
        if provider == "nordvpn":
            try:
                self._nordvpn
            except AttributeError:
                self._nordvpn = NordVpn()
            self._proxy = self._nordvpn
            self._set_proxy(self._proxy.server(usr, pwd, nation))
        else:
            raise NotImplementedError("Provider {} not implemented".format(provider))

    def _try_tor(self):
        self._proxy = None
        if self._canUseTor:
            self._set_proxy(Tor(self._tor_passphrase).server())
            log.warning("Setting tor proxy")
        else:
            # TODO settare default proxy
            log.warning("Scraping with you IP")

    def _set_random_user_agent(self):
        random_ua = self._ua_obj.random
        self._ua = random_ua
        log.debug("UserAgent selected {}".format(random_ua))

    def _proxy_wrapper(self, url: str, request_type: str, times: int, max_repeat: int = 5, **kwargs):
        success = False
        res = None
        try:
            # scraper = cloudscraper.create_scraper()
            # scraper.proxies = self.proxies
            # return scraper.get(url, proxies=self.proxies, **kwargs)

            headers = kwargs.pop("headers") if "headers" in kwargs else {}
            headers["User-Agent"] = self._ua
            if request_type == "get":
                params = kwargs.pop("params") if "params" in kwargs else None
                res = requests.get(url, params=params, timeout=3, proxies=self.proxies, headers=headers, **kwargs)
            elif request_type == "post":
                data = kwargs.pop("data") if "data" in kwargs else None
                json = kwargs.pop("json") if "json" in kwargs else None
                res = requests.post(url, data=data, json=json, timeout=3, proxies=self.proxies, headers=headers,
                                    **kwargs)
            else:
                raise NotImplementedError("only get and post please")
            success = True
        # username and pwd do not work
        except ProxyError as e:
            if self._proxy is not None:
                log.debug("Proxy {} {} not valid".format(self._proxy.usr, self._proxy.pwd))
                self._db.update_result(self._proxy.usr, self._proxy.pwd, False, self._proxy.name)
        # server do not work
        except ConnectTimeout as e:
            if self._proxy is not None:
                self._proxy.remove_proxy()

        except ConnectionError and ConnectionAbortedError and ConnectionRefusedError and ConnectionResetError:
            log.error("Get a stable connection please")
        finally:
            if not success:
                self.hide(force=True)
                times += 1
                if times == max_repeat:
                    times = 0
                else:
                    return self._proxy_wrapper(url, request_type, times, **kwargs)
            return res
