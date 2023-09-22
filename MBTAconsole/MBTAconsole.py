import requests
from requests.exceptions import HTTPError
from requests.auth import HTTPBasicAuth
import pprint
from collections import defaultdict, deque
from itertools import combinations

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
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}') 
    except Exception as err:
        print(f'Other error occurred: {err}')
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

def build_connection_graph(connecting_stops):
    connection_graph = defaultdict(set)
    for routes in connecting_stops.values():
        for source, dest in  combinations(routes, 2):
            connection_graph[source].add(dest)
            connection_graph[dest].add(source)
    return connection_graph

def BFS_algo(graph, source, sink):
	q = deque([[source]])
	visited = []
	if source == sink:
		print("Those are the same stops")
		return
	while q:
		path = q.popleft()
		node = path[-1]
		if node not in visited:
			for route in graph[node]:
				new_path = list(path)
				new_path.append(route)
				q.append(new_path)
				if route == sink:
					return new_path
		visited.append(node)

def find_route(start, end):
    routes = get_routes()
    stop_dict = build_stop_dict(routes)
    connecting_stops = dict(filter(lambda x:len(x[1])>1, stop_dict.items()))
    connection_graph = build_connection_graph(connecting_stops)
    connection_graph[start] = stop_dict[start]
    for route in stop_dict[end]:
         connection_graph[route].add(end)
    path = BFS_algo(connection_graph,start,end)
    print(f"\n{start} to {end} -> {', '.join(path[1:-1])}\n")
    
            





