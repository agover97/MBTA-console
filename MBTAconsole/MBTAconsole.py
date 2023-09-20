import requests
from requests.exceptions import HTTPError

__URL__ = "https://api-v3.mbta.com/"

def query_MBTA():
    try:
        response = requests.get(__URL__)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')

def hello():
    print("hellow world")

