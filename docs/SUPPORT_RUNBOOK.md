# SUPPORT_RUNBOOK - MAS-004_VJ6530-ZBC-Bridge

## 1. Positioning
- Subproject dependent on `MAS-004_RPI-Databridge` orchestration.

## 2. Local Setup
- `python -m venv .venv`
- `.\.venv\Scripts\Activate.ps1`
- `python -m pip install -U pip`
- `python -m pip install -e .`

## 3. Pi Deployment
- Pull:
  - `ssh mas004-rpi "cd /opt/MAS-004_VJ6530-ZBC-Bridge && git pull --ff-only"`
- Restart:
  - `ssh mas004-rpi "sudo systemctl restart mas004-vj6530-zbc-bridge.service"`
- Logs:
  - `ssh mas004-rpi "sudo journalctl -u mas004-vj6530-zbc-bridge.service -n 120 --no-pager"`

## 4. Verification
- Service active.
- Config values (`host`, `port`, `timeout_s`, `simulation`) are valid.
- Probe output stable (`tcp ok`/expected failures only).
- For protocol changes, verify packet parsing/building paths in `protocol.py`.

## 5. Sync Rule
- Use main repo scripts:
  - `MAS-004_RPI-Databridge/scripts/mas004_multirepo_status.ps1`
  - `MAS-004_RPI-Databridge/scripts/mas004_multirepo_sync.ps1`
- Never auto-overwrite dirty Pi repos.
