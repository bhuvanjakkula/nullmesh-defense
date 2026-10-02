from nullmesh.routing import RoutingTable

def demo():
    r=RoutingTable()
    for a,b in [('A','B'),('B','C'),('C','D'),('A','D')]: r.add_link(a,b)
    print('A -> C next hop:', r.next_hop('A','C'))
    r.remove_link('B','C'); print('after B-C failure:', r.next_hop('A','C'))
if __name__=='__main__': demo()
