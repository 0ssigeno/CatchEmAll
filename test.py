import logging as log

from PokedexOwned.youporn import youporn
from manage_requests import ManageRequests

if __name__ == "__main__":
    log.basicConfig(level=log.INFO, format='%(threadName)s %(message)s')
    creds = "usr:pwd"
    usr = creds.split(":")[0]
    pwd = creds.split(":")[1]
    print(youporn(usr, pwd, ManageRequests()))
