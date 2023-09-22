import pytest
from MBTAconsole.MBTAconsole import get_routes, build_stop_dict, build_connection_graph

@pytest.fixture()
def routes():
    print("setup")
    yield get_routes()
    print("teardown")

class TestResource:
    def test_get_routes(self, routes):
        assert len(routes) == 8

    def test_build_stop_dict(self, routes):
        stop_dict = build_stop_dict(routes)
        assert len(stop_dict) > 0
    
    def test_build_connection_graph(self, routes):
        stop_dict = build_stop_dict(routes)
        connecting_stops = dict(filter(lambda x:len(x[1])>1, stop_dict.items()))
        connection_graph = build_connection_graph(connecting_stops)
        assert len(connection_graph) > 0
        
