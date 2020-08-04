import requests
from bs4 import BeautifulSoup

from catchEmAll.pokedex.pokeball import Pokeball


def netflix(poke: Pokeball):
    usr, pwd = poke.get_account()
    site_url = "https://www.netflix.com/Login"

    res = poke.requests_function(requests.get, site_url)

    soup = BeautifulSoup(res.text, features="html.parser")
    auth_url = soup.find('input', attrs={'name': 'authURL'})['value']

    # Post request to login
    res = poke.requests_function(requests.post, site_url,
                                 data={'email': usr,
                                       'password': pwd,
                                       'rememberMe': True,
                                       'flow': 'websiteSignUp',
                                       'mode': 'login',
                                       'action': 'loginAction',
                                       'withFields': 'email,password,rememberMe,nextPage',
                                       'authURL': auth_url,
                                       'nextPage': 'https://www.netflix.com/viewingactivity'
                                       })
    if 'Login' not in res.url:
        return True
    else:
        return False
