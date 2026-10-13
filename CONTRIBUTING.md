# 🤝 Beitragen

Danke für dein Interesse an **StingBox – ehrlich erklärt**! Companion-Repos: [node300-net/firewalla-gold-pro-msp](https://github.com/node300-net/firewalla-gold-pro-msp) · [node300-net/sovereign-datacenter](https://github.com/node300-net/sovereign-datacenter).

## Grundsätze

1. **Ehrlich bleiben.** Keine erfundenen Features, Preise oder Tests. Jede Aussage braucht einen **Link** oder die Markierung **⚠️ unverifiziert / Schätzung / Ableitung** mit Begründung.
2. **Primärquelle vor Hörensagen.** Herstellerseiten = ✅, Foren/Reddit/Reviews = 🟦 (Einzelmeinung). Kundenzitate auf der Herstellerseite sind **kein** Beleg.
3. **Datum nennen.** Preise, OS-Versionen und Features ändern sich. Bei Änderungen den **Recherchestand** aktualisieren.
4. **Herstellerneutral.** Kein Affiliate-Link, keine Werbesprache. Schwächen gehören in den [Reality Check](docs/reality-check.md) – auch die der Alternativen.
5. **Keine Secrets.** Keine StingBox-Codes (Aufkleber!), API-Keys, Subscription-Codes, öffentlichen IPs oder HackerCam-Links mit Session-Code.
6. **Sprache.** Dokumentation auf **Deutsch**; Fachbegriffe (Honeypot, Webhook, Lateral Movement …) dürfen Englisch bleiben.

## Workflow

```bash
git checkout -b docs/kurze-beschreibung
# Änderungen …
git add -A
git commit -m "docs: StingBox-Preise auf Stand 2026-11 aktualisiert"   # docs:/feat:/fix:/chore:
# Pull Request mit Quellen-Links + Hinweis, welche Tabellen betroffen sind
```

## Besonders willkommen

- 🧪 **Praxiserfahrungen** mit einer echten StingBox (Alarm-Latenz, Fehlalarme, OS-Version via Debug-Datei, Netzteil 230 V)
- 🔌 Das tatsächliche **JSON-Format** der API-Antworten (anonymisiert) → Poller verbessern
- ⚖️ Antworten des Herstellers zu DPA/Datenstandort/SSH-Key ([Fragenkatalog](docs/reality-check.md#-fragen-die-du-dem-hersteller-vor-dem-kauf-stellen-solltest))
- 🐤 Getestete **OpenCanary**-Configs für das Lab (LXC, Alerting via Webhook/SMTP)

## Lizenz

Mit deinem Beitrag akzeptierst du: Code/Configs unter **MIT**, Doku unter **CC BY-SA 4.0** (siehe [LICENSE](LICENSE)).
