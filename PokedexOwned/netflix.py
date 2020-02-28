from bs4 import BeautifulSoup

from manage_requests import ManageRequests


def netflix(usr: str, pwd: str, mr: ManageRequests):
    site_url = "https://www.netflix.com/Login"

    res = mr.get_with_checks(site_url, headers={'User-Agent': 'Mozilla/5.0'})

    if res:
        soup = BeautifulSoup(res.text, features="html.parser")
        auth_url = soup.find('input', attrs={'name': 'authURL'})['value']

        # Post request to login
        res = mr.post_with_checks(site_url,
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
        mr.clear_cookies()
        if 'Login' not in res.url:
            return True
        else:
            return False
    else:
        mr.clear_cookies()
        return False
