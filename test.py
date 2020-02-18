from functions import *
from manage_requests import ManageRequests

creds = "test:test"
usr = creds.split(":")[0]
pwd = creds.split(":")[1]
mr = ManageRequests()
uplay(usr, pwd, mr)
