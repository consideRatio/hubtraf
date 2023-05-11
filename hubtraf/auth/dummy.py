import time


async def login_dummy(session, hub_url, log, username, password):
    """
    Log in username with password to hub_url in aiohttp session.

    log is used to emit timing and status information.
    """
    start_time = time.monotonic()

    url = hub_url / 'hub/login'

    # get login page, should set xsrf cookie in the session
    try:
        resp = await session.get(url)
    except Exception as e:
        log.msg(
            "Login: Failed to get login page with exception {}".format(repr(e)),
            action="login",
            phase="failed",
            duration=time.monotonic() - start_time,
        )
        return False

    if resp.status != 200:
        log.msg(
            "Login: Failed to get login page with response {}".format(str(resp)),
            action="login",
            phase="failed",
            duration=time.monotonic() - start_time,
        )
        return False

    hub_cookies = session.cookie_jar.filter_cookies(url)
    if "_xsrf" in hub_cookies:
        _xsrf = hub_cookies["_xsrf"].value
    else:
        _xsrf = ""

    try:
        resp = await session.post(
            url,
            data={
                "username": username,
                "password": password,
                "_xsrf": _xsrf,
            },
            allow_redirects=False,
        )
    except Exception as e:
        log.msg('Login: Failed with exception {}'.format(repr(e)), action='login', phase='failed', duration=time.monotonic() - start_time)
        return False
    if resp.status != 302:
        log.msg('Login: Failed with response {}'.format(str(resp)), action='login', phase='failed', duration=time.monotonic() - start_time)
        return False
    return True
