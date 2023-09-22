'''
asx_api_checker.py - Call Post API and filter output

Author: Christian Ricci - 22/Sept/2023
Usage: python asx_api_checker.py <json file>

# ChangeLog:
22/Sept/2023 - created
23/Sept/2023 - added input and output key validation method to make code simpler

# TODO:
* Improve logger to show type of message, move stack trace to a different log
* Use argparse to parmetrize constants
* Use dataclass and dataclass(json) to create and validate a json schema
* Save the output into a separate file
* May need to handlde status_code (201,202,204)
'''

import traceback
import sys
import json
import logging
import requests

API_ENDPOINT = "https://localhost:8000/service/generate"
API_HEADERS = { "content-type": "application/json", "authentication": "onetime-long-string" }
JSON_INPUT_SEARCH_KEY = 'private'
JSON_INPUT_SEARCH_VALUE = False
JSON_OUTPUT_SEARCH_KEY = 'valid'
JSON_OUTPUT_SEARCH_VALUE = True

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

debug_handler = logging.FileHandler('debug.log')
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(debug_handler)

def main(input_json_file):
    input_json = open(input_json_file, 'r')
    data = validation(input_json)
    input_json.close()
    
    for key in data:
        if(input_key_exist(data, key)):
            logger.info(f'Generating results for input key: {key}')
            payload = json.dumps(data.get(key))
            response = call_post_api(API_ENDPOINT, payload, API_HEADERS)
            filter_results(response, JSON_OUTPUT_SEARCH_KEY, JSON_OUTPUT_SEARCH_VALUE)

def input_key_exist(data_dict, key):
    return (data_dict.get(key) and not data_dict.get(key).get(JSON_INPUT_SEARCH_KEY))

def filter_results(input_json, filter_key, filter_value):
    """
    This function will take care of producing results
        input_json : str, json object
        filter_key : str, json key to search
        filter_value : str, json value to search
    return:
        status : bool, true (data found), false (no data found)
    """
    status = False
    data = validation(input_json)
    try:
        for key in data:
            if(output_key_exist(data, key, filter_key, filter_value)):
                logger.info(key)
                status = True
        return status
    except AttributeError as e:
        logger.error(f'Input json key {filter_key} must exist in the input json file.')
        raise e
    except Exception as e:
        raise e

def output_key_exist(data_dict, key, filter_key, filter_value):
    return (data_dict.get(key) and data_dict.get(key).get(filter_key) == filter_value)

def call_post_api(endpoint, payload, headers):
    """
    call POST api
        endpoint : str, url of the rest api server
        payload : str, post api data payload
        headers : dict, post api headers
    return:
        content : str, the api output
    """
    try:
        response = requests.post(url=endpoint, data=payload, headers=headers)
        if(response.status_code != 200):
            raise Exception(f'POST request return status_code: {response.status_code}')
        return response.content.decode('utf8')
    except Exception as e:
        logger.error("There is a problem calling the post api. payload: %s", payload)
        raise e

def validation(input_json):
    """
    Json content validation
        input_json : str | io (object), the source json file
    return:
        json : dict | json data
    """
    try:
        json_data = json.loads(input_json) if input_json.__class__.__name__ == 'str' else json.load(input_json)
        return json_data
    except Exception as e:
        raise ValueError("Not a valid json format")

if __name__ == "__main__":
    logger.info('Program started')
    
    if(len(sys.argv) <= 1):
        logger.error("Please specify the json file as first argument.\nUsage: python asx_api_checker.py <json file>")
        exit(1)
    
    try:
        main(sys.argv[1])
    except Exception as e:
        logger.debug(e, stack_info=True,exc_info=True)
        logger.error("Program finished with errors.")
        exit(1)
    
    logger.info("Program finished")