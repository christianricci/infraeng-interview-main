import json
from unittest import mock
import pytest
import os
import requests
from coding.asx_api_checker import call_post_api, filter_results, validation

FIXTURES = f'{os.getcwd()}/coding/test/fixtures'
API_ENDPOINT = "http://localhost:8000/service/generate"
API_HEADERS = { "content-type": "application/json", "authentication": "onetime-long-string" }
JSON_INPUT_SEARCH_KEY = 'private'
JSON_INPUT_SEARCH_VALUE = False
JSON_OUTPUT_SEARCH_KEY = 'valid'
JSON_OUTPUT_SEARCH_VALUE = True

@pytest.fixture
def get_file_valid_json():
    return open(f'{FIXTURES}/valid-format.json','r')

def test_validation_when_valid_input_file(get_file_valid_json):
    """produce a valid json output when reading a valid json file

    Args:
        get_file_valid_json (io): io pointer of the file
    """
    json_data = validation(get_file_valid_json)
    
    assert len(json.dumps(json_data)) > 0
    assert json_data.__class__ == dict().__class__

@pytest.fixture
def get_file_invalid_json():
    return open(f'{FIXTURES}/invalid-format.json','r')

def test_validation_when_invalid_input_file(get_file_invalid_json):
    """raise exception when reading an invalid json file

    Args:
        get_file_invalid_json (io): io pointer of the file
    """
    with pytest.raises(ValueError) as ex:
        json_data = validation(get_file_valid_json)
    
    assert str(ex.value) == "Not a valid json format"

@pytest.fixture
def get_string_valid_json():
    return '{"dummy": 1}'

def test_validation_when_valid_input_is_string(get_string_valid_json):
    """produce a valid json output when reading a valid json string

    Args:
        get_string_valid_json (str|b): json string
    """
    json_data = validation(get_string_valid_json)
    
    assert len(json.dumps(json_data)) > 0
    assert json_data.__class__ == dict().__class__

@pytest.fixture
def get_string_invalid_json():
    return 'invalid json'

def test_validation_when_invalid_input_is_string(get_string_invalid_json):
    """raise exception when reading an invalid json string

    Args:
        get_string_invalid_json (str|b): not a valijson string
    """
    with pytest.raises(ValueError) as ex:
        json_data = validation(get_string_valid_json)
    
    assert str(ex.value) == "Not a valid json format"

@pytest.fixture
def mock_valid_request():
    mock_response = mock.Mock()
    mock_response.content = b'{"dummy":1}'
    mock_response.status_code = 200
    return mock.patch.object(requests, 'post', return_value=mock_response)

def test_call_post_api_onvalid_response_return_content(mock_valid_request):
    """validate api call produce a json output

    Args:
        mock_valid_request (mock.object): mock of requests object
    """
    with mock_valid_request:
        response = call_post_api(API_ENDPOINT, 'some.payload', headers=API_HEADERS)
    
    assert len(json.dumps(response)) > 0
    assert json.loads(response).__class__ == dict().__class__

@pytest.fixture
def get_filter_results_with_found_payload():
    data = open(f'{FIXTURES}/filter-found-response.json','r')
    return json.dumps(json.load(data))
    
def test_filter_results_when_response_has_matching_data(get_filter_results_with_found_payload):
    """Return True when json output from API call contains the filter pattern matching

    Args:
        get_filter_results_with_found_payload (str): json string
    """
    status = filter_results(get_filter_results_with_found_payload, JSON_OUTPUT_SEARCH_KEY, JSON_OUTPUT_SEARCH_VALUE)
    
    assert status == True
    
@pytest.fixture
def get_filter_results_without_found_payload():
    data = open(f'{FIXTURES}/filter-nofound-response.json','r')
    return json.dumps(json.load(data))
    
def test_filter_results_when_response_has_no_matching_data(get_filter_results_without_found_payload):
    """Return False when json output from API call does not contains the filter pattern matching

    Args:
        get_filter_results_without_found_payload (str): json string
    """
    status = filter_results(get_filter_results_without_found_payload, JSON_OUTPUT_SEARCH_KEY, JSON_OUTPUT_SEARCH_VALUE)
    
    assert status == False