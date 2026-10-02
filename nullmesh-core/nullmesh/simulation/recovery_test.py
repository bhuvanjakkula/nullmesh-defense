from nullmesh.reconciliation import missing_ids
print('objects needed after reconnection:', sorted(missing_ids({'a','b'}, {'b','c','d'})))
