import requests

from functions import *
from manage_requests import ManageRequests

if __name__ == "__main__":
    log.basicConfig(level=log.INFO, format='%(threadName)s %(message)s')
    usr = creds.split(":")[0]
    pwd = creds.split(":")[1]
    mr = ManageRequests()
    server = mr.nordvpn.get_working_server()
    # nordvpn(usr, pwd, mr)
    proxies = {"https": "https://{}:{}@{}:80".format(usr, pwd, server)}
    res = requests.get("https://www.google.com", proxies=proxies)
    print(res.status_code)
