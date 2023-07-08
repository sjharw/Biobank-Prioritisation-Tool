import requests
import pytest
import responses
import re
from configparser import ConfigParser
from functions.utils import get_url

# Path import from config.ini
config = ConfigParser()
config.read("config.ini")


def test_get_request_sucess():
    """ Test for successful request """
    # set up response object that gives success status 200
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, 'https://api.example.com/data',
                 json={'data': 'example'}, status=200)
        response = get_url('https://api.example.com/data')
        assert response.status_code == 200
        assert response.json() == {'data': 'example'}

def test_get_request_failed_responsecode():
    """ Test for failed request """
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET, 
            'https://api.example.com/data',
            json={'error': 'Request failed'},
            status=500
        )
        with pytest.raises(requests.exceptions.HTTPError) as exc_info:
            get_url('https://api.example.com/data')
        assert str(exc_info.value) == "HTTPError. Request failed with response status: 500, see the following link for more detail on this status: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500"

def test_get_request_failed_token():
    """ Test for failed request """
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET, 
            'https://api.example.com/data',
            body='{"message":"Token not valid!"}',
            content_type='application/json', 
            status=200
        )
        with pytest.raises(requests.exceptions.HTTPError) as exc_info:
            get_url('https://api.example.com/data')
        assert str(exc_info.value) == "Token not valid!"

def test_get_request_failed_url():
    """ Test for failed request """
    with pytest.raises(requests.exceptions.ConnectionError) as exc_info:
        get_url('https://api.example.com/invalid-url')
    # Get unique 
    error_message_result = str(exc_info.value)
    # Regular expression pattern
    pattern = r'0x[0-9a-fA-F]+'
    # Search for the pattern in the string
    match = re.search(pattern, error_message_result)
    error_message_expected = f"Connection Error. Error connecting to server url:https://api.example.com/invalid-url. Following error raised: HTTPSConnectionPool(host='api.example.com', port=443): Max retries exceeded with url: /invalid-url (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at {match.group()}>: Failed to establish a new connection: [Errno 11001] getaddrinfo failed'))"
    assert error_message_result == error_message_expected