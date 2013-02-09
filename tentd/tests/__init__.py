"""Pytentd test suite"""

__all__ = ['GET', 'PUT', 'POST', 'HEAD']

from flask import current_app, json, url_for, g
from py.test import main

from tentd.lib.flask import JSONEncoder

class HTTP(object):
    """HTTP convenience functions that take an endpoint name,
    and optionally data or JSON to send"""
    
    def __init__(self, function_name):
        """Creates a HTTP function using the name of the method that will be
        called on ``current_app.client``"""
        self.function_name = function_name

    def __call__(self, endpoint, data=None, secure=False,
        content_type='text/html', **kwargs):
        """Call current_app.client.<function> and return the response.

        The endpoint argument is used to build an url using url_for, along
        with **kwargs. If it starts with a /, it is used as-is. If the data
        argument is a dict or list, it will be dumped to JSON"""
        if not endpoint[0] == '/':
            endpoint = url_for(endpoint, **kwargs)
        
        if isinstance(data, (dict, list)):
            data = json.dumps(data, cls=JSONEncoder)
            content_type = 'application/json'

        if not hasattr(current_app, 'client'):
            raise NotImplementedError(
                "The application requires a test client")

        if secure:
            raise NotImplementedError(
                "Secure requests are not yet implemented")

        # Fetch and call the function from the client
        http_function = getattr(current_app.client, self.function_name)
        return http_function(endpoint, data=data, content_type=content_type)

GET, PUT, POST, HEAD = HTTP('get'), HTTP('put'), HTTP('post'), HTTP('head')

def profile_url_for(entity, _external=False):
    """Get an entity profile url without using url_for"""
    url = ['/profile']

    if not current_app.single_user_mode:
        url.append('/' + entity.name)

    if _external:
        url.append('http://' + current_app.config['SERVER_NAME'])

    return ''.join(url[::-1])

def response_has_link_header(response):
    """Test that a response includes an entity link header"""
    link = '<{}>; rel="https://tent.io/rels/profile"'.format(
        profile_url_for(g.entity, _external=True))
    return response.headers['Link'] == link

if __name__ == '__main__':
    main()
