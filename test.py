import requests

from functions import *
from manage_requests import ManageRequests

if __name__ == "__main__":
    log.basicConfig(level=log.INFO, format='%(threadName)s %(message)s')
    creds = "username:password"
    usr = creds.split(":")[0]
    pwd = creds.split(":")[1]
    mr = ManageRequests()
    nordvpn(usr, pwd, mr)
    