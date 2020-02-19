from functions import *
from manage_requests import ManageRequests

if __name__ == '__main__':
    creds = "username:password"
    usr = creds.split(":")[0]
    pwd = creds.split(":")[1]
    mr = ManageRequests()
    youporn(usr, pwd, mr)
