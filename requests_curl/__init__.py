import logging
import sys
import urllib
from json import dumps

import requests

logger = logging.getLogger('requests_curl')

functions = (
    'request',
    'get',
    'options',
    'head',
    'post',
    'put',
    'patch',
    'delete',
)
originals = {}


def get_headers(headers):
    return ' '.join([
        "-H '{}:{}'".format(key, val) for (key, val) in headers.items()
    ])


def request(method, url, **kwargs):
    response = originals['request'](method, url, **kwargs)
    logger.debug("curl -X {} {} '{}'".format(
        response.request.method,
        get_headers(response.request.headers),
        response.url
    ))
    return response


def get(url, params=None, **kwargs):
    response = originals['get'](url, params=params, **kwargs)
    logger.debug("curl -L {} '{}'".format(
        get_headers(response.request.headers),
        response.url
    ))
    return response


def options(url, **kwargs):
    response = originals['options'](url, **kwargs)
    logger.debug("curl -L -X OPTIONS {} '{}'".format(
        get_headers(response.request.headers),
        response.url
    ))
    return response


def head(url, **kwargs):
    response = originals['head'](url, **kwargs)
    logger.debug("curl -L -X HEAD {} '{}'".format(
        get_headers(response.request.headers),
        response.url
    ))
    return response


def post(url, data=None, json=None, **kwargs):
    response = originals['post'](url, data=data, json=json, **kwargs)

    data_option = ''
    if data:
        data_option = "--data-urlencode '{}'".format(urllib.parse.urlencode(data))
    elif json:
        data_option = "--data '{}'".format(dumps(json))

    logger.debug("curl -X POST {} {} '{}'".format(
        data_option,
        get_headers(response.request.headers),
        response.url
    ))
    return response


def put(url, data=None, **kwargs):
    response = originals['put'](url, data=data, **kwargs)

    data_option = ''
    if data:
        data_option = "--data-urlencode '{}'".format(urllib.parse.urlencode(data))

    logger.debug("curl -X PUT {} {} '{}'".format(
        data_option,
        get_headers(response.request.headers),
        response.url
    ))
    return response


def patch(url, data=None, **kwargs):
    response = originals['patch'](url, data=data, **kwargs)

    data_option = ''
    if data:
        data_option = "--data-urlencode '{}'".format(urllib.parse.urlencode(data))

    logger.debug("curl -X PATCH {} {} '{}'".format(
        data_option,
        get_headers(response.request.headers),
        response.url
    ))
    return response


def delete(url, **kwargs):
    response = originals['delete'](url, **kwargs)
    logger.debug("curl -X DELETE {} '{}'".format(
        get_headers(response.request.headers),
        response.url
    ))
    return response


for func in functions:
    originals[func] = getattr(requests, func)
    setattr(requests, func, getattr(sys.modules[__name__], func))
