from nullmesh.routing import RoutingTable
r=RoutingTable(); r.add_link('A','B'); r.add_link('C','D')
print('partitioned route A->D:', r.next_hop('A','D'))
r.add_link('B','C'); print('recovered route A->D:', r.next_hop('A','D'))
