# 🧰 configs/ – Beispiele für die Lab-Integration

> Zurück zur [README](../README.md) · Kontext: [docs/integration.md](../docs/integration.md)

> [!CAUTION]
> **Alles hier ist ⚠️ ungetestet gegen eine echte StingBox.** Die Dateien setzen die [öffentliche API-Doku (Jan. 2026)](https://stingbox.twocyber.com/api_doc/StingBoxAPIDocumentation.pdf) und die [FAQ](https://www.stingbox.com/faq/) um. Das genaue JSON-Antwortformat ist dort nicht spezifiziert – der Poller ist deshalb bewusst tolerant geschrieben. Platzhalter: `<<…>>`, `10.10.10.250`.

| Datei | Zweck | Ziel |
|---|---|---|
| [`stingbox-api-poller.py`](stingbox-api-poller.py) | Holt `getLatestAlerts` per API (nur ausgehend), dedupliziert, schreibt nach lokalem Syslog | Node 3 |
| [`stingbox-api-poller.service`](stingbox-api-poller.service) · [`stingbox-api-poller.timer`](stingbox-api-poller.timer) | systemd-Oneshot + Timer (60 s) | Node 3 |
| [`rsyslog-stingbox.conf`](rsyslog-stingbox.conf) | Sortiert Tag `stingbox` nach `/var/log/remote/stingbox.log` | Node 3 |
| [`suricata-decoy.rules`](suricata-decoy.rules) | Suricata-Regeln: jeder Zugriff auf den Köder = Alarm | Node 3 |
| [`firewalla-stingbox-rules.yaml`](firewalla-stingbox-rules.yaml) | Regelkonzept (kein Importformat!) für Egress-Härtung | Firewalla App/MSP |
| [`huawei-stingbox-port.example`](huawei-stingbox-port.example) | Access-Port, Port-Security, SPAN-Quelle | Huawei S220S ⚠️ |

Lizenz: **MIT** (Code) – siehe [LICENSE](../LICENSE).
