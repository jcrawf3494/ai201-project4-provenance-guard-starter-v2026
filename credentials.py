"""
The verified-human credential store. ← STRETCH ITEM

A writer who completes an extra step — typing an attestation phrase exactly —
earns a credential: a random token tied to their `creator_id`. Later, a
submission that carries a valid credential for its creator is stamped
`verified_human: true`, and that stamp travels onto the item in the `/submit`
response, the audit log, and `GET /content/<id>`.

This is a deliberate, low-tech design. It does not *prove* a human wrote the
text — nothing here could. It proves the writer took a named step and claimed
authorship on the record, which is exactly what a credential on a writing site
is: an accountable claim, not a detector.

The store is file-backed JSON so credentials survive a restart. One token per
creator; re-verifying replaces the old token.
"""

import json
import secrets
import threading
from datetime import datetime, timezone

import config

_lock = threading.Lock()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _read() -> dict:
    if not config.CREDENTIALS_FILE.exists():
        return {}
    try:
        return json.loads(config.CREDENTIALS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _write(store: dict) -> None:
    config.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    config.CREDENTIALS_FILE.write_text(
        json.dumps(store, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def issue(creator_id: str) -> str:
    """
    Issue (or replace) a credential for a creator and return the token.

    The token is what the writer keeps and sends back on `/submit`.
    """
    token = secrets.token_urlsafe(16)
    with _lock:
        store = _read()
        store[creator_id] = {"credential": token, "verified_at": _now()}
        _write(store)
    return token


def verify(creator_id: str, credential: str) -> bool:
    """True if this credential is the one currently issued to this creator."""
    if not isinstance(creator_id, str) or not isinstance(credential, str):
        return False
    record = _read().get(creator_id)
    return bool(record) and secrets.compare_digest(
        record.get("credential", ""), credential
    )


def is_verified(creator_id: str) -> bool:
    """True if this creator holds any credential at all."""
    return creator_id in _read()
