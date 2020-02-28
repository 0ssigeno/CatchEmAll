import logging as log
from base64 import b64encode

from manage_requests import ManageRequests


def uplay(usr: str, pwd: str, mr: ManageRequests):
    site_post = "https://public-ubiservices.ubi.com/v3/profiles/sessions"
    credentials = str.encode(usr + ":" + pwd)
    encoding = b64encode(credentials).decode()
    res = mr.post_with_checks(site_post, headers={"Content-Type": "application/json",
                                                  "Ubi-AppId": "e06033f4-28a4-43fb-8313-6c2d882bc4a6",
                                                  "Authorization": "Basic " + encoding})
    mr.clear_cookies()
    if res:
        if res.status_code == 200:
            return True
        else:
            return False
    else:
        decode = res.content.decode("utf-8")
        if "Invalid credentials" in decode or "Authentication forbidden" in decode:
            return False
        elif "Too many calls" in decode:
            log.debug("Uplay problem")
            mr.set_random_proxy()
            mr.set_random_user_agent()
            return uplay(usr, pwd, mr)
        else:
            log.debug("Uplay problem")
            mr.set_random_proxy()
            mr.set_random_user_agent()
            return uplay(usr, pwd, mr)
