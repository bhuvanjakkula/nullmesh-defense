from nullmesh.routing import RoutingTable

def test_reroute():
    r=RoutingTable(); r.add_link('A','B'); r.add_link('B','C'); r.add_link('A','D'); r.add_link('D','C')
    assert r.next_hop('A','C') in {'B','D'}
    r.remove_link('A','B'); assert r.next_hop('A','C') == 'D'
