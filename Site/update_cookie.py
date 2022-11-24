from Site import session


def update_cookie() -> str:
    endpoint = 'https://onlinepatent.ru/trademarks'
    session.get(endpoint)
    return session.cookies.get('f_session_key')