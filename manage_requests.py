import logging as log
import random
import re
from enum import Enum

import cloudscraper
from fake_useragent import UserAgent
from mysql.connector.errors import ProgrammingError
from requests.exceptions import ProxyError

from Proxies.nordvpn import NordVpn
from Proxies.tor import Tor
from manage_db import ManageDb


class Proxies(Enum):
    NORDVPN = "nordvpnProxy"
    TOR = "torProxy"


# TODO magari un parametro passato da ES su ogni quanto cambiare paese
PROXIES_IMPLEMENTED = {Proxies.NORDVPN: NordVpn(requests_before_change_country=10),
                       Proxies.TOR: Tor()}
WEIGHTS = [0.8, 0.2]


class ManageRequests:
    def __init__(self, local: bool = True):
        self._req = cloudscraper.create_scraper()
        self.db = ManageDb(local)
        self._proxyName = None
        self._proxyUsr = None
        self._proxyPwd = None
        self._ua = UserAgent()
        log.info("Init MR done")

    def update_headers(self, headers: dict):
        self._req.headers.update(headers)

    def clear_cookies(self):
        self._req.cookies.clear()

    def bypass_cf(self, site):
        """
        Cloudflare return a cookie, default is cf_token, but to be sure we save every single cookie in a dict to be used
        inside requests
        """
        cookies = self._req.get_cookie_string(site)[0]
        cookies = re.split("[;=]", cookies)
        return dict(zip(*[iter(cookies)] * 2))

    """
        nordvpnProxy disponibile
    """

    def set_random_proxy(self):
        """
        Retrieve a random vpn provider
        Retrieve every user that can be used as proxy
        Retrieve a server to use the credentials
        Set the proxy and the value for the class
        """
        if PROXIES_IMPLEMENTED:
            # We have weights now, so you can use the favourite proxy more
            provider = random.choices(list(PROXIES_IMPLEMENTED.keys()), weights=WEIGHTS, k=1)

            # TODO se domani crasha, fai la retrieve di un enum e non del valore corrispondente
            if provider == Proxies.NORDVPN:
                users = None
                try:
                    users = self.db.retrieve_users(provider, True)
                except ProgrammingError as e:
                    log.warning("You don't have a nordvpnProxy column, BE CAREFUL you are scraping with you IP")
                    self.db.add_column(provider)
                if users:
                    credentials = random.choice(users)
                    usr = credentials[0]
                    pwd = credentials[1]
                    server = PROXIES_IMPLEMENTED[provider].get_random_server()
                    self._req.proxies = {"https": "https://{}:{}@{}:80".format(usr, pwd, server)}
                    self._proxyName = provider
                    self._proxyUsr = usr
                    self._proxyPwd = pwd
                    log.info("Setting proxy to {}@{}:80".format(usr, server))
                else:
                    log.warning("No proxy available for nordvpn")
            elif provider == Proxies.TOR:
                server = PROXIES_IMPLEMENTED[provider].get_random_server()

            else:
                raise Exception("Provider not implemented")
        else:
            raise Exception("Please implement at least one proxy")

    def set_random_user_agent(self):
        """
        Guess what, set a random user agents for the following requests
        """
        random_ua = self._ua.random
        self.update_headers({"User-Agent": random_ua})
        log.info("UserAgent selected {}".format(random_ua))

    def get_with_checks(self, site: str, cookies: dict = None, headers: dict = None):
        try:
            res = self._req.get(site, cookies=cookies, headers=headers)
            return res
        except ProxyError as e:
            if self._proxyUsr:
                log.warning("Proxy {} {} not valid".format(self._proxyUsr, self._proxyPwd))
                self.db.update_result(self._proxyUsr, self._proxyPwd, self._proxyName, False)
            else:
                log.warning("Big uff ")
            self.set_random_proxy()
            return self.get_with_checks(site, headers=headers, cookies=cookies)
        except ConnectionError and ConnectionAbortedError and ConnectionRefusedError and ConnectionResetError:
            log.error("Get a stable connection please")
            exit()

    def post_with_checks(self, site: str, data: dict = None, cookies: dict = None, headers: dict = None):
        """
        Makes a post request as `requests` but checks that the proxy works
        If it doesn't, the user will be setted as unusuable for the future and another proxy is selected to repeat the
        post request
        """
        try:
            res = self._req.post(site, data=data, cookies=cookies, headers=headers)
            return res
        except ProxyError as e:
            if self._proxyUsr:
                log.warning("Proxy {} {} not valid".format(self._proxyUsr, self._proxyPwd))
                self.db.update_result(self._proxyUsr, self._proxyPwd, self._proxyName, False)
            else:
                log.warning("Big uff ")
            self.set_random_proxy()
            return self.post_with_checks(site, data=data, cookies=cookies, headers=headers)
        except ConnectionError and ConnectionAbortedError and ConnectionRefusedError and ConnectionResetError:
            log.error("Get a stable connection please")
            exit()
