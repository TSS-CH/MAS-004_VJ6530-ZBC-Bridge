# MAS-004_VJ6530-ZBC-Bridge

Bridge-Client und Daemon fuer Videojet 6530 (TTO) ueber ZBC Binary Protocol.

## Enthalten
- `client.py`: Bridge-Wrapper auf `MAS-004_ZBC-Library`
- `_zbc_library.py`: Import/Fallback auf das benachbarte Repo `MAS-004_ZBC-Library`
- `mapper.py`: Legacy-Value-Codecs und Kompatibilitaets-Helfer
- `service.py`: Daemon und CLI fuer Probe, Summary, Current-Parameter-Read/Write

## Service-Dateien
- `systemd/mas004-vj6530-zbc-bridge.service`
- `scripts/install.sh`
- `scripts/run.sh`
- `scripts/default_config.json`

## Installation auf Raspi
```bash
cd /opt/MAS-004_VJ6530-ZBC-Bridge
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
chmod +x scripts/*.sh
./scripts/install.sh
```

## Config
`/etc/mas004_vj6530_zbc_bridge/config.json`

- `enabled`: Service aktiv/inaktiv
- `simulation`: wenn `true`, keine Live-Verbindung
- `host`, `port`: Drucker Endpoint
- `timeout_s`, `poll_interval_s`

ZBC-Standardport fuer den 6530 ist hier `3002`.

## Manuelle Live-Pruefung
```bash
cd /opt/MAS-004_VJ6530-ZBC-Bridge
./.venv/bin/python -m mas004_vj6530_zbc_bridge --config /etc/mas004_vj6530_zbc_bridge/config.json --summary-json
```

## Current-Parameter lesen
```bash
./.venv/bin/python -m mas004_vj6530_zbc_bridge --config /etc/mas004_vj6530_zbc_bridge/config.json \
  --read-current-parameter System/TCPIP/BinaryCommsNetworkPort2
```

## Current-Parameter schreiben
```bash
./.venv/bin/python -m mas004_vj6530_zbc_bridge --config /etc/mas004_vj6530_zbc_bridge/config.json \
  --write-current-parameter System/TCPIP/JobUpdateReplyDelay 1
```

## Live verifiziert
- `MAS-004_ZBC-Library` ist jetzt die gemeinsame ZBC-Basis.
- `FTX` mit File-Typ `CURRENT_PARAMETERS (0x0009)` wurde gegen den echten 6530 erfolgreich verifiziert.
- Kontrollierter Writeback-Nachweis:
  - `System/TCPIP/JobUpdateReplyDelay` live `0 -> 1 -> 0`
  - jeder Schritt vom Drucker mit `NUL` bestaetigt und anschliessend wieder ausgelesen
