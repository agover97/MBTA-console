import requests
from requests.exceptions import HTTPError
import pprint

class Route:
    def __init__(self, name, id, stops):
         self._name = name
         self._id = id
         self._stops = stops 
      
    def name(self):
        return self._name
      
    def id(self):
        return self._id

    def stops(self):
        return self._stops

class Stop:
    def __init__(self, name, id):
        self._name = name
        self._id = id

    def name(self):
        return self._name 

    def id(self):
        return self._id

__URL__ = "https://api-v3.mbta.com/"

def query_MBTA(endpoint):
    token = 'af6a9e7a2d084a36889b298194e10d94'
    headers = {'Authorization': f'Token {token}'}
    try:
        response = requests.get(__URL__ + endpoint, headers=headers)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        return response.json()

def get_routes():
    endpoint = "routes?filter[type]=0,1"
    data = query_MBTA(endpoint)["data"]
    routes = []
    for route in data:
        route_name = route['attributes']['long_name']
        route_id = route["id"]
        stops = get_stops(route_id)
        routes.append(Route(route_name,route_id,stops))
    return routes

def get_stops(route_id):
    endpoint = "stops?filter[route]=" + route_id
    data = query_MBTA(endpoint)["data"]
    stops = []
    for stop in data:
        stop_name = stop["attributes"]["name"]
        stop_id = stop["id"]
        stops.append(Stop(stop_name,stop_id))
    return stops

def get_long_names():
    routes = get_routes()
    print("The MBTA has these subway routes:")
    for route in routes:
        print(route.name())

