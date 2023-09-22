import pytest
from MBTAconsole.MBTAconsole import get_routes

@pytest.fixture()
def routes():
    print("setup")
    yield get_routes()
    print("teardown")

class TestResource:
    def test_get_routes(self, routes):
        assert len(routes) == 8



    
