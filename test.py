import logging as log

import requests

from Proxies.nordvpn import NordVpn
from Proxies.tor import Tor
from manage_requests import ManageRequests

if __name__ == "__main__":
    log.basicConfig(level=log.INFO, format='%(threadName)s %(message)s')
    creds = "user:pass"
    usr = creds.split(":")[0]
    pwd = creds.split(":")[1]
    mr = ManageRequests()
    # mr.set_random_proxy()
    # tor = Tor()
    nordvpn = NordVpn()
    # proxies = {"https": tor.get_random_server()}
    proxies = {"https": nordvpn.get_random_server()}
    # mr.set_random_user_agent()
    res = requests.get("https://www.expressvpn.com/what-is-my-ip", proxies=proxies)
    print(res.content)
