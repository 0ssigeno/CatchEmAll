import logging as log
from json import loads

from bs4 import BeautifulSoup

from manage_requests import ManageRequests


def pornhub(usr: str, pwd: str, mr: ManageRequests):
    post_url = "https://www.pornhub.com/front/authenticate"
    get_url = "https://www.pornhub.com/"
    # Get main page with redirect and token
    res = mr.get_with_checks(get_url, headers={'User-Agent': 'Mozilla/5.0'})
    # Filter out redirect and token
    soup = BeautifulSoup(res.text, features="html.parser")
    token = soup.find('input', attrs={'name': 'token'})
    if token:
        token = token['value']
        # Post request to login
        res = mr.post_with_checks(post_url,
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
        mr.clear_cookies()
        mr.set_random_proxy()
        mr.set_random_user_agent()
        return pornhub(usr, pwd, mr)
    mr.clear_cookies()
    if int(loads(res.content)["success"]) == 1:
        return True
    else:
        return False
