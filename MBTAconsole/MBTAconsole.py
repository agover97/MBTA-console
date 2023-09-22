import requests
from requests.exceptions import HTTPError
from requests.auth import HTTPBasicAuth
import pprint
from collections import defaultdict, deque
from itertools import combinations

class Route:
    """
    A class used to represent subway route
    """
    def __init__(self, name, id, stops):
        """
        Parameters
        ----------
        name : str
            The long name of the subway route (e.g. "Red Line")
        id : str
            The id of the subway route. Used as endpoint for MPTA api. (e.g. "Red")
        stops : list[Stop]
            The list of stops on subway line
        """
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
    """
    A class used to represent subway stop
    """
    def __init__(self, name, id):
        """
        Parameters
        ----------
        name : str
            The name of the stop (e.g. "Park Street")
        id : str
            The id of the stop. Used as endpoint for MPTA api (e.g. "place-pktrm")
        """
        self._name = name
        self._id = id

    def name(self):
        return self._name 

    def id(self):
        return self._id

__URL__ = "https://api-v3.mbta.com/"


def query_MBTA(endpoint):
    """
    Submit REST request to MBTA api and handle response

    Parameters
    ----------
    endpoint : str
        endpoint to be appended to base URL

    Returns
    -------
    dict
        json formatted response of request
    """
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
    """
    Build list of routes by querying MBTA api

    Parameters
    ----------
    none

    Returns
    -------
    list[Route]
        list of route objects representing MBTA subways
    """
    #Filter routes on server side so less data is returned
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
    """
    Build list of stops

    Parameters
    ----------
    route_id : str
        endpoint of a specific subway line to appended to URL (e.g. "Red")

    Returns
    -------
    list[Stops]
        list of stops on a given subway line
    """
    endpoint = "stops?filter[route]=" + route_id
    data = query_MBTA(endpoint)["data"]
    stops = []
    for stop in data:
        stop_name = stop["attributes"]["name"]
        stop_id = stop["id"]
        stops.append(Stop(stop_name,stop_id))
    return stops

def get_long_names():
    """
    Prints the names of all subway line
    """
    routes = get_routes()
    print("The MBTA has these subway routes:")
    for route in routes:
        print(route.name())

def get_longest_route():
    """
    Prints the name and number of stops for the longest subway line
    """
    routes = get_routes()
    greatest = max(routes, key=lambda route:len(route.stops()))
    print(f"The {greatest.name()} has the greatest number of stops: {len(greatest.stops())} stops")

def get_shortest_route():
    """
    Prints the name and number of stops
    """
    routes = get_routes()
    fewest = min(routes, key=lambda route:len(route.stops()))
    print(f"The {fewest.name()} has the fewest number of stops: {len(fewest.stops())} stops")

def build_stop_dict(routes):
    """
    Build a dictionary of all stops on all lines where the key is the stop name and the value is a list of routes that stop is on

    Parameters
    ----------
    routes : list[Route]
        list of Route objects for each subway line

    Returns
    -------
    dict{ str : list[str] }
        dictionary mapping stop name to subway route name
    """
    stop_dict = defaultdict(list)
    for route in routes:
        for stop in route.stops():
            stop_dict[stop.name()].append(route.name())
    return stop_dict

def get_connecting_stops():
    """
    Build a dictionary of all stops that connect two or more subway lines. Calls build_stop_dict and filters results.

    Parameters
    ----------
    none

    Returns
    -------
    dict{ str : list[str] }
        dictionary mapping stop name to list of subway route names
    """
    routes = get_routes()
    stop_dict = build_stop_dict(routes)
    connecting_stops = dict(filter(lambda x:len(x[1])>1, stop_dict.items()))
    print("\nThe following stops connect 2 or more subway routes:\n")
    for stop, connectors in sorted(connecting_stops.items()):
        print(f"{stop} : {', '.join(connectors)}")

def build_connection_graph(connecting_stops):
    """
    Build a dictionary which maps each subway route to all other routes which can be access by sharing a connecting stop

    Parameters
    ----------
    connecting_stops : dict{ str : list[str] }
        dictionary of all stops that connect two or more subway lines

    Returns
    -------
    dict{ str : list[str] }
        dictionary mapping subway route name to list of subway route names
    """
    connection_graph = defaultdict(set)
    for routes in connecting_stops.values():
        for source, dest in  combinations(routes, 2):
            connection_graph[source].add(dest)
            connection_graph[dest].add(source)
    return connection_graph

def BFS_algo(graph, source, sink):
    """
    Find shortest path from source to sink node along graph

    Parameters
    ----------
    graph : dict{ str : list[str] }
        dictionary representing graph, key is node, value is list of neighbors
    source : str
        key of starting node
    sink : str
        key of end node

    Returns
    -------
    list[str]
        list of node names comprising shortest path from source to sink
    """
    q = deque([[source]])
    visited = []
    if source == sink:
        print("Those are the same stops")
        return []
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
    """
    Find list of subway line changes to get from stop:start to stop:end

    Prints list of changes if valid route is found

    If invalid stop names submitted prints message saying input was invlaid and prints list of all subway stops

    Parameters
    ----------
    start : str
        name of starting stop
    end : str
        name of destination stop

    Returns
    -------
    none
    """
    routes = get_routes()
    stop_dict = build_stop_dict(routes)
    connecting_stops = dict(filter(lambda x:len(x[1])>1, stop_dict.items()))
    connection_graph = build_connection_graph(connecting_stops)
    if start in stop_dict and end in stop_dict:
        connection_graph[start] = stop_dict[start]
        for route in stop_dict[end]:
            connection_graph[route].add(end)
        path = BFS_algo(connection_graph,start,end)
        if len(path) > 2:
            print(f"\n{start} to {end} -> {', '.join(path[1:-1])}\n")
    else:
        if start not in stop_dict:
            print(f"{start} is not a valid stop")
        if end not in stop_dict:
            print(f"{end} is not a valid stop")
        print(f"Please select stops from the following list. If the name of the stop contains a space use quotes \" \"")
        for stop in sorted(stop_dict.keys()):
             print(stop)
    
            





