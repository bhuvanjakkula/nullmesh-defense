# NullMesh v0.1

NullMesh is a **civilian/defensive reference prototype** for disruption-tolerant, partition-aware networking. It demonstrates cryptographic node identity, signed immutable messages, persistent store-and-forward delivery, duplicate suppression, peer discovery, and topology/routing primitives.

It is deliberately **not** an "indestructible" network and contains no offensive cyber, stealth/evasion, weapon-control, targeting, or unauthorized-access features.

## Architecture

Each node owns an Ed25519 identity and SQLite object store. Messages are immutable signed objects. Nodes discover explicitly configured HTTP peers, validate received objects, store them locally, and retry forwarding when connectivity is available. The routing module provides a small graph/alternate-path primitive used by simulations and as a foundation for future transport-aware routing.

> Security note: v0.1 signs messages but does **not** provide payload confidentiality. Do not send secrets through this prototype. A production design should add reviewed end-to-end authenticated encryption, credential lifecycle/revocation, authorization, replay controls, rate limits, secure transport, and external security review.

## Run locally

Requires Python 3.11+.

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e '.[test]'
pytest -q
NULLMESH_NODE=node-a NULLMESH_DATA=./data-a nullmesh serve --port 8001
```

Open `http://localhost:8001/docs` for the API UI.

## Run four nodes with Docker

```bash
docker compose up --build
```

Node APIs are exposed on ports 8001-8004. Query a node identity:

```bash
curl http://localhost:8001/v1/info
curl http://localhost:8003/v1/info
```

Take the `node_id` from the destination and submit a message:

```bash
curl -X POST http://localhost:8001/v1/send \
  -H 'content-type: application/json' \
  -d '{"destination":"DESTINATION_NODE_ID","payload":"hello","priority":5}'
```

Inspect stored/delivered objects:

```bash
curl http://localhost:8003/v1/objects
```

## Failure simulation

The pure routing simulations are safe and deterministic:

```bash
python simulation/topology.py
python simulation/partition_test.py
python simulation/recovery_test.py
```

For the Docker topology, stopping a container models an ordinary node/link outage. Restarting it lets queued forwarding resume.

## Protocol object

A `MeshObject` contains an ID, source/destination IDs, timestamp, priority, payload, payload hash, source public key, Ed25519 signature, and hop history. Receivers reject a mismatched payload hash or invalid signature and suppress duplicate object IDs.

## Current limitations / roadmap

v0.1 is an educational reference implementation. Important future work includes encrypted payload envelopes, authenticated peer sessions, explicit trust/authorization policy, route advertisements, acknowledgements, retry/backoff, TTL enforcement, conflict-free replicated metadata, bandwidth-aware scheduling, transport plugins, metrics, fuzz/property testing, and formal protocol documentation.

## License

MIT; see `LICENSE`.
