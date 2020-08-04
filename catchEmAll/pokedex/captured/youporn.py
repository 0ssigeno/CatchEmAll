import requests

from catchEmAll.pokedex.pokeball import Pokeball


def youporn(poke: Pokeball):
    usr, pwd = poke.get_account()
    post_url = "https://www.youporn.com/login/"
    # Post request to login
    res = poke.requests_function(requests.post, post_url,
                                 data={'login[username]': usr,
                                       'login[password]': pwd,
                                       'login[previous]': '',
                                       'login[logical_data': '{}',
                                       })
    # mr.clear_cookies()
    # TODO has some false positive
    if "Bad credentials" in str(res.text):
        return False
    else:
        return True
