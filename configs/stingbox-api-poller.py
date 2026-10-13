#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
stingbox-api-poller.py - StingBox-Alarme per API abholen und ins lokale Syslog schreiben.

Warum Pull? Syslog/Webhook der StingBox werden (sehr wahrscheinlich) aus der Hersteller-Cloud
zugestellt und braeuchten einen aus dem Internet erreichbaren Empfaenger. Pull ist nur ausgehend
und holt verpasste Alarme nach (Webhooks haben laut FAQ keinen Retry).

Quelle API: https://stingbox.twocyber.com/api_doc/StingBoxAPIDocumentation.pdf (Jan. 2026)
  POST https://stingbox.twocyber.com/threat2/api/stingbox_api.php
  Felder: api_key=<KEY>, api_data={"action":"getLatestAlerts"}   (liefert die letzten 100 Alarme)

WARNUNG: Ungetestet gegen eine echte StingBox. Das JSON-Antwortformat ist nicht dokumentiert;
der Code akzeptiert daher Liste ODER Objekt mit einer Liste darin.

Nur Python-Standardbibliothek.
"""
import argparse
import hashlib
import json
import logging
import logging.handlers
import os
import sys
import urllib.parse
import urllib.request

API_URL = "https://stingbox.twocyber.com/threat2/api/stingbox_api.php"
DEFAULT_KEY_FILE = "/etc/stingbox/api_key"
DEFAULT_STATE = "/var/lib/stingbox-poller/seen.json"
MAX_SEEN = 2000  # deutlich mehr als die 100 Alarme pro Abruf


def read_key(path: str) -> str:
    env = os.environ.get("STINGBOX_API_KEY")
    if env:
        return env.strip()
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read().strip()


def fetch(action: str, key: str, timeout: int = 20):
    # Key als POST-Feld (nicht in der URL), damit er nicht in Proxy-/Access-Logs landet.
    body = urllib.parse.urlencode(
        {"api_key": key, "api_data": json.dumps({"action": action})}
    ).encode()
    req = urllib.request.Request(
        API_URL, data=body, method="POST",
        headers={"User-Agent": "node300-stingbox-poller/0.1"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def extract_alerts(payload):
    """Tolerant: Liste direkt, oder erste Liste in einem Objekt (z. B. {"alerts": [...]})."""
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for k in ("alerts", "data", "result", "results"):
            if isinstance(payload.get(k), list):
                return payload[k]
        for v in payload.values():
            if isinstance(v, list):
                return v
    return []


def fingerprint(alert) -> str:
    raw = json.dumps(alert, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(raw.encode()).hexdigest()


def load_state(path: str) -> list:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_state(path: str, seen: list) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(seen[-MAX_SEEN:], fh)
    os.replace(tmp, path)


def make_logger(address: str) -> logging.Logger:
    log = logging.getLogger("stingbox")
    log.setLevel(logging.INFO)
    if address.startswith("/"):
        handler = logging.handlers.SysLogHandler(address=address)
    else:
        host, _, port = address.partition(":")
        handler = logging.handlers.SysLogHandler(address=(host, int(port or 514)))
    handler.setFormatter(logging.Formatter("stingbox: %(message)s"))
    log.addHandler(handler)
    return log


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--key-file", default=DEFAULT_KEY_FILE)
    ap.add_argument("--state", default=DEFAULT_STATE)
    ap.add_argument("--syslog", default="/dev/log", help="/dev/log oder host:port (UDP)")
    ap.add_argument("--once", action="store_true", help="einmal abrufen (fuer systemd-Timer)")
    ap.add_argument("--dry-run", action="store_true", help="nur ausgeben, nichts senden/speichern")
    args = ap.parse_args()

    try:
        key = read_key(args.key_file)
    except OSError as exc:
        print(f"API-Key nicht lesbar: {exc}", file=sys.stderr)
        return 2

    try:
        payload = fetch("getLatestAlerts", key)
    except Exception as exc:  # Netzwerk/JSON - beim naechsten Timer-Lauf erneut
        print(f"API-Abruf fehlgeschlagen: {exc}", file=sys.stderr)
        return 1

    alerts = extract_alerts(payload)
    seen = load_state(args.state)
    seen_set = set(seen)
    new = [a for a in alerts if fingerprint(a) not in seen_set]

    log = None if args.dry_run else make_logger(args.syslog)
    # Aelteste zuerst senden (API-Reihenfolge unbekannt -> nach timestamp, falls vorhanden)
    new.sort(key=lambda a: str(a.get("timestamp", "")) if isinstance(a, dict) else "")
    for a in new:
        line = a.get("cef") if isinstance(a, dict) and a.get("cef") else json.dumps(a, ensure_ascii=False)
        if args.dry_run:
            print(line)
        else:
            log.warning(line)
        seen.append(fingerprint(a))

    if not args.dry_run:
        save_state(args.state, seen)
    print(f"{len(alerts)} Alarme abgerufen, {len(new)} neu.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
