def get_url(req, path=''):
    return '{}://{}/{}'.format(get_scheme(req), req.host, path.lstrip('/'))


def get_ip(req):
    ip = req.headers.get(
        'X-Forwarded-For',
        req.headers.get('X-Real-IP', None))
    if ip is not None:
        return ip
    peername = req.transport.get_extra_info('peername')
    if peername is not None:
        host, port = peername
        return host
    return 'unknown'


def get_scheme(req):
    scheme = req.headers.get(
        'X-Forwarded-Protocol',
        req.headers.get(
            'X-Scheme',
            req.headers.get('X-Forwarded-Proto', None)))

    if scheme:
        return scheme

    return req.scheme
