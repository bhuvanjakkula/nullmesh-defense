from nullmesh.routing import RoutingTable

def test_partition_and_recovery():
    r=RoutingTable(); r.add_link('A','B'); r.add_link('C','D')
    assert r.next_hop('A','D') is None
    r.add_link('B','C'); assert r.next_hop('A','D') == 'B'
