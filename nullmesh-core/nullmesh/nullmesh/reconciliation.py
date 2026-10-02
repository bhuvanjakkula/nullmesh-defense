"""Deterministic duplicate suppression/reconciliation for immutable objects."""
def missing_ids(local_ids: set[str], remote_ids: set[str]) -> set[str]:
    return remote_ids - local_ids
