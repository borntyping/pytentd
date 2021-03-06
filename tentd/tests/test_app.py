"""Test the pytentd application"""

from flask import url_for, g
from py.test import mark, raises
from werkzeug.exceptions import ImATeapot, NotFound

from tentd.documents import CoreProfile
from tentd.tests import GET, profile_url_for, response_has_link_header
from tentd.tests.conftest import SINGLE, MULTIPLE, SUBDOMAINS

def test_expected_profile_url(request, app, entity):
    url = profile_url_for(entity)
    if app.test_mode is SINGLE:
        assert url == '/profile'
    elif app.test_mode is MULTIPLE:
        assert url == '/' + entity.name + '/profile'
    elif app.test_mode is SUBDOMAINS:
        assert url == 'http://{}.example.com/profile'.format(entity.name)

def test_url_value_preprocessor(app, entity):
    """Assert urls are created correctly in single user mode"""
    assert url_for('entity.profiles') == profile_url_for(entity)

def test_url_defaults(app, entity):
    """Assert that the url defaults are working"""
    assert GET('entity.profiles')

def test_link_header(app, entity):
    """Assert that the link header is added"""
    assert response_has_link_header(GET('entity.profiles'))

def test_coffee(app):
    """Test that /coffee raises an exception"""
    with raises(ImATeapot):
        assert GET('coffee')
