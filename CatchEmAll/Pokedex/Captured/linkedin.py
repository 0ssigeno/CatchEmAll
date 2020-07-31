from bs4 import BeautifulSoup

from CatchEmAll.Requests.proxy_requests import ProxyRequest


def linkedin(usr: str, pwd: str, pr: ProxyRequest):
    get_url = "https://www.linkedin.com/login"
    post_url = "https://www.linkedin.com/checkpoint/lg/login-submit"

    # Get main page with tokens
    res = pr.get(get_url)
    # Filter out tokens
    soup = BeautifulSoup(res.text, features="html.parser")
    csrf_token = soup.find('input', attrs={'name': 'csrfToken'})['value']
    s_id_string = soup.find('input', attrs={'name': 'sIdString'})['value']
    login_csrf_param = soup.find('input', attrs={'name': 'loginCsrfParam'})['value']

    # Post request to login
    res = pr.post(post_url,
                  data={'session_key': usr,
                        'session_password': pwd,
                        'csrfToken': csrf_token,
                        'sIdString': s_id_string,
                        'loginCsrfParam': login_csrf_param,
                        })
    # pr.clear_cookies()
    if 'login' not in res.url:
        if 'challenge' not in res.url:
            return True
        else:
            # TODO Linkedin asks for a code sended to the email, we put a True for now but we can not really access
            #  the account
            return True
    else:
        return False
