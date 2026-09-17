from __future__ import annotations
import hashlib, json
from .io import atomic_write_json


def digest_object(obj):
    payload = dict(obj)
    payload.pop('ticket_digest', None)
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()


def issue_ticket(path, ticket):
    ticket = dict(ticket)
    ticket['ticket_digest'] = digest_object(ticket)
    atomic_write_json(path, ticket)
    return ticket


def load_ticket(path):
    obj = json.loads(path.read_text(encoding='utf-8'))
    if obj.get('ticket_digest') != digest_object(obj):
        raise ValueError('ticket digest mismatch')
    return obj
