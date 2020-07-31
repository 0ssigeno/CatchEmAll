from catchEmAll.proxyrequests.proxy_requests import ProxyRequest


def spotify(usr: str, pwd: str, mr: ProxyRequest):
    """
    Todo complete
    """
    site_get = "https://accounts.spotify.com/it/login"
    cookies = mr.get_with_checks(site_get).cookies.get_dict()
    csrf = cookies["csrf_token"]
    cookies["__bon"] = "MHwwfC00ODY2MjU5N3wtMjA0MzgyOTA3NHwxfDF8MXwx"  # Non me gusta hardcodarlo
    site_post = site_get
    site_post = "https://accounts.spotify.com/password/login/"
    mr.update_headers({"content-length": str(9999)})
    recaptcha = "3AOLTBLTG3vkAxIqYcJpKqDtD25hvebW9hG0YOMwv5" \
                "-WR9V3HefOgKmKbEFGeloLzjOHilwU7qZlrj6YiI4C5kg83j283SYUoZKeqvOXhL" \
                "-AGXGR8PygVup5Ae58MQNCdfFTPXkWpFrb_NUB3XrbKXVasonIKqUhFGcv91PWzVBw3Nsx" \
                "-GlAeAqn2pz5uVVzQpVzssSZCs6ocBj9J_Bsuwln2GrQFfcgehsI7Pzv8aIfdSmVsSSBvTup6xBWbtRq2nUrigADfF8DrLmS1aRGuOTEFOvmYPwDA8GPchAtO-bx9GrIRkXkBlFJ-P4ZEix6fNxheA0tywNncAA67rg-G3gq8avBJG33P4Wvs9GHrxGbh8GSEnZ6IEdRkRTb9RhrIlQTGukAclGId "
    res = mr.post_with_checks(site_post, data={"username": usr, "password": pwd, "csrf_token": csrf},
                              cookies=cookies)
