import requests
from requests.exceptions import HTTPError
from requests.auth import HTTPBasicAuth
import pprint
from collections import defaultdict

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
    try:
        response = requests.get(__URL__ + endpoint)
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

def get_longest_route():
    routes = get_routes()
    greatest = max(routes, key=lambda route:len(route.stops()))
    print(f"The {greatest.name()} has the greatest number of stops: {len(greatest.stops())} stops")

def get_shortest_route():
    routes = get_routes()
    fewest = min(routes, key=lambda route:len(route.stops()))
    print(f"The {fewest.name()} has the fewest number of stops: {len(fewest.stops())} stops")

def build_stop_dict(routes):
    stop_dict = defaultdict(list)
    for route in routes:
        for stop in route.stops():
            stop_dict[stop.name()].append(route.name())
    return stop_dict

def get_connecting_stops():
    routes = get_routes()
    stop_dict = build_stop_dict(routes)
    connecting_stops = dict(filter(lambda x:len(x[1])>1, stop_dict.items()))
    print("\nThe following stops connect 2 or more subwy routes:\n")
    for stop, connectors in sorted(connecting_stops.items()):
        print(f"{stop} : {', '.join(connectors)}")



