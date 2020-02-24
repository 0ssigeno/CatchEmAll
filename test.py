from functions import *
from manage_requests import ManageRequests

if __name__ == "__main__":
    # log.basicConfig(level=log.INFO, format='%(threadName)s %(message)s')
    creds = "user:pass"
    usr = creds.split(":")[0]
    pwd = creds.split(":")[1]
    mr = ManageRequests()
    mr.set_random_proxy()
    mr.set_random_user_agent()
    netflix(usr, pwd, mr)
