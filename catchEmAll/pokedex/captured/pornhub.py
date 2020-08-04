import logging as log
from json import loads

import requests
from bs4 import BeautifulSoup

from catchEmAll.pokedex.pokeball import Pokeball


def pornhub(poke: Pokeball):
    usr, pwd = poke.get_account()
    post_url = "https://www.pornhub.com/front/authenticate"
    get_url = "https://www.pornhub.com/"
    # Get main page with redirect and token
    res = poke.requests_function(requests.get, get_url)
    # Filter out redirect and token
    soup = BeautifulSoup(res.text, features="html.parser")
    token = soup.find('input', attrs={'name': 'token'})
    if token:
        token = token['value']
        # Post request to login
        res = poke.requests_function(requests.post, post_url,
                                     data={'username': usr,
                                           'password': pwd,
                                           'subscribe': 'undefined',
                                           'setSendTip': 'false',
                                           'remember_me': '0',
                                           'from': 'pc_login_modal_:index',
                                           'token': token,
                                           })
    else:
        log.debug("Pornhub problem")
        return None
    mr.clear_cookies()
    if int(loads(res.content)["success"]) == 1:
        return True
    else:
        return False
