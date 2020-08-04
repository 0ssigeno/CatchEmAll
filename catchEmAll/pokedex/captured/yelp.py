from logging import debug

import requests
from bs4 import BeautifulSoup

from catchEmAll.pokedex.pokeball import Pokeball


def yelp(poke: Pokeball):
    usr, pwd = poke.get_account()
    site_url = "https://www.yelp.co.uk/login"
    # Get main page with csrf_token
    res = poke.requests_function(requests.get, site_url)
    # Filter out csrf_token value
    soup = BeautifulSoup(res.text, features="html.parser")
    try:
        csrf_token = soup.find('form', id='ajax-login').find('input', 'csrf_token')['value']
        # Post request to login
        res = poke.requests_function(requests.post, site_url,
                                     data={'email': usr,
                                           'password': pwd,
                                           'csrf_token': csrf_token
                                           })

        if res:
            if 'login' not in res.url:
                return True
            else:
                return False
        else:
            raise Exception("Yelp step 0 not implemented")

    except TypeError:
        if "Are you a human" in res.content.decode("utf-8"):
            # TODO bypass recaptcha
            debug("Must implement recaptcha for Yelp")
            return False
        else:
            raise Exception("Yelp step 1 not implemented")
    except AttributeError:
        if "not allowed to access" in res.content.decode("utf-8"):
            debug("Must do something (?) for Yelp")
            return False
        else:
            raise Exception("Yelp step 2 not implemented")
