import urllib.request as _urllib
import json as _json

def _http_request(method, url, data=None, headers=None):
    if headers is None:
        headers = {}
    req = _urllib.Request(url, data=data, headers=headers, method=method)
    try:
        resp = _urllib.urlopen(req)
        body = resp.read().decode('utf-8')
        return {'status': resp.getcode(), 'headers': dict(resp.headers), 'body': body}
    except Exception as e:
        return {'status': 0, 'headers': {}, 'body': str(e)}

def _http_get(url, headers=None):
    return _http_request('GET', url, headers=headers)

def _http_post(url, data, headers=None, content_type='application/json'):
    if headers is None:
        headers = {}
    if isinstance(data, (dict, list)):
        data = _json.dumps(data).encode('utf-8')
        headers['Content-Type'] = content_type
    else:
        data = str(data).encode('utf-8')
    return _http_request('POST', url, data, headers)

def _http_put(url, data, headers=None):
    if headers is None:
        headers = {}
    if isinstance(data, (dict, list)):
        data = _json.dumps(data).encode('utf-8')
        headers['Content-Type'] = 'application/json'
    else:
        data = str(data).encode('utf-8')
    return _http_request('PUT', url, data, headers)

def _http_delete(url, headers=None):
    return _http_request('DELETE', url, headers=headers)

_httptable = {
    'get': _http_get,
    'post': _http_post,
    'put': _http_put,
    'delete': _http_delete,
    'request': _http_request,
  }
