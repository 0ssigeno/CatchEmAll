import logging as log
from base64 import b64encode

import requests

from catchEmAll.pokedex.pokeball import Pokeball


def uplay(poke: Pokeball):
    usr, pwd = poke.get_account()
    site_post = "https://public-ubiservices.ubi.com/v3/profiles/sessions"
    credentials = str.encode(usr + ":" + pwd)
    encoding = b64encode(credentials).decode()
    res = poke.requests_function(requests.post, site_post, headers={"Content-Type": "application/json",
                                                                    "Ubi-AppId": "e06033f4-28a4-43fb-8313-6c2d882bc4a6",
                                                                    "Authorization": "Basic " + encoding})
    # pr.clear_cookies()
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
            return None
        else:
            log.debug("Uplay problem")
            return None
