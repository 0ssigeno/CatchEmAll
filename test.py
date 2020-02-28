import logging as log

import functions
from manage_requests import ManageRequests

if __name__ == "__main__":
    log.basicConfig(level=log.INFO, format='%(threadName)s %(message)s')
    creds = "aaron1998evans@gmail.com:aaron1998"
    usr = creds.split(":")[0]
    pwd = creds.split(":")[1]
    print(functions.pornhub(usr, pwd, ManageRequests()))
