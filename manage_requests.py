import logging as log
import random
import re

import cloudscraper
from fake_useragent import UserAgent
from requests.exceptions import ProxyError

from Vpn.nordvpn import NordVpn
from manage_db import ManageDb

PROXIES_IMPLEMENTED = {"nordvpnProxy":NordVpn()}


class ManageRequests:
    def __init__(self, local=True):
        self.req = cloudscraper.create_scraper()
        self.db = ManageDb(local)
        self.proxyName = None
        self.proxyUsr = None
        self.proxyPwd = None
        self.ua = UserAgent()
        log.info("Init MR")

    def bypass_cf(self, site):
        """
        Cloudflare return a cookie, default is cf_token, but to be sure we save every single cookie in a dict to be used
        inside requests
        """
        cookies = self.req.get_cookie_string(site)[0]
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
            provider = random.choice(list(PROXIES_IMPLEMENTED.keys()))
            if provider == "nordvpnProxy":
                users = self.db.retrieve_users(provider, True)
                if users:
                    creds = random.choice(users)
                    usr = creds[0]
                    pwd = creds[1]
                    server = PROXIES_IMPLEMENTED[provider].get_random_server()
                    self.req.proxies = {"https": "https://{}:{}@{}:80".format(usr, pwd, server)}
                    self.proxyName = provider
                    self.proxyUsr = usr
                    self.proxyPwd = pwd
                    log.info("Setting proxy to {}@{}:80".format(usr, server))
                else:
                    log.warning("No proxy available for nordvpn")
            else:
                raise Exception("Provider not implemented")
        else:
            raise Exception("Please implement at least one proxy")

    def set_random_user_agent(self):
        """
        Guess what, set a random user agents for the following requests
        """
        random_ua = self.ua.random
        self.req.headers.update({"User-Agent": random_ua})
        log.info("UserAgent selected {}".format(random_ua))

    def get_with_checks(self, site, cookies=None, headers=None):
        try:
            res = self.req.get(site, cookies=cookies, headers=headers)
            return res
        except ProxyError as e:
            if self.proxyUsr:
                log.warning("Proxy {} {} not valid".format(self.proxyUsr, self.proxyPwd))
                self.db.update_result(self.proxyUsr, self.proxyPwd, self.proxyName, False)
            else:
                log.warning("Big uff ")
            self.set_random_proxy()
            return self.get_with_checks(site, headers=headers, cookies=cookies)
        except ConnectionError and ConnectionAbortedError and ConnectionRefusedError and ConnectionResetError:
            log.error("Get a stable connection please")
            exit()

    def post_with_checks(self, site, data=None, cookies=None):
        """
        Makes a post request as `requests` but checks that the proxy works
        If it doesn't, the user will be setted as unusuable for the future and another proxy is selected to repeat the
        post request
        """
        try:
            res = self.req.post(site, data=data, cookies=cookies)
            return res
        except ProxyError as e:
            if self.proxyUsr:
                log.warning("Proxy {} {} not valid".format(self.proxyUsr, self.proxyPwd))
                self.db.update_result(self.proxyUsr, self.proxyPwd, self.proxyName, False)
            else:
                log.warning("Big uff ")
            self.set_random_proxy()
            return self.post_with_checks(site, data=data, cookies=cookies)
        except ConnectionError and ConnectionAbortedError and ConnectionRefusedError and ConnectionResetError:
            log.error("Get a stable connection please")
            exit()
