from logging import debug

from bs4 import BeautifulSoup

from CatchEmAll.Requests.proxy_requests import ProxyRequest


def yelp(usr: str, pwd: str, mr: ProxyRequest):
    site_url = "https://www.yelp.co.uk/login"

    # Get main page with csrf_token
    res = mr.get_with_checks(site_url, headers={'User-Agent': 'Mozilla/5.0'})
    # Filter out csrf_token value
    soup = BeautifulSoup(res.text, features="html.parser")
    try:
        csrf_token = soup.find('form', id='ajax-login').find('input', 'csrf_token')['value']
        # Post request to login
        res = mr.post_with_checks(site_url,
                                  data={'email': usr,
                                        'password': pwd,
                                        'csrf_token': csrf_token
                                        })

        mr.clear_cookies()
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
