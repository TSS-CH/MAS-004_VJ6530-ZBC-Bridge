# SUPPORT_CHANGELOG - MAS-004_VJ6530-ZBC-Bridge

## 2026-03-13
- Bridge switched to `MAS-004_ZBC-Library`:
  - shared profile detection
  - shared ZBC transport/framing
  - shared summary parsing
  - shared current-parameter archive handling
- Added import shim `_zbc_library.py`:
  - uses installed package or sibling repo `../MAS-004_ZBC-Library`
- `service.py` extended:
  - real ZBC probe instead of raw TCP connect
  - `--summary-json`
  - `--read-current-parameter`
  - `--write-current-parameter`
- Corrected standard ZBC port in config to `3002`.
- Live confirmed:
  - `FTX[CURRENT_PARAMETERS]` accepted by the 6530
  - controlled writeback `JobUpdateReplyDelay 0 -> 1 -> 0`

## 2026-03-04
- Added support memory files:
  - `docs/PROJECT_CONTEXT.md`
  - `docs/SUPPORT_RUNBOOK.md`
  - `docs/SUPPORT_CHANGELOG.md`
- Captured protocol-oriented support boundaries vs main Databridge.
- Baseline local HEAD during this entry: `556c73e`.

## Maintenance Rule
- Update this changelog on framing/checksum behavior, mapper/codec rules, deployment flow, or integration contract changes.
