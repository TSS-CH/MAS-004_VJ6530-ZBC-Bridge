# PROJECT_CONTEXT - MAS-004_VJ6530-ZBC-Bridge

## Role in MAS-004
- Subproject (not orchestration owner).
- Provides Videojet 6530 connectivity via ZBC binary protocol.
- Intended to be integrated by the main Databridge project.

## Repository Scope
- Package: `mas004_vj6530_zbc_bridge/`
- ZBC framing/checksum: `protocol.py`
- TCP client transaction logic: `client.py`
- Mapping/value codec support: `mapper.py`
- Probe service loop: `service.py`
- Config model: `config.py`

## Protocol Summary
- Packet framing: `0xA5 ... 0xE4`
- Header checksum + optional CRC16 payload checksum
- ACK/NAK transport flags supported

## Runtime Paths
- Config: `/etc/mas004_vj6530_zbc_bridge/config.json`
- Systemd unit: `mas004-vj6530-zbc-bridge.service`
- Pi repo path: `/opt/MAS-004_VJ6530-ZBC-Bridge`

## Integration Boundary
- Repository focus is transport/protocol fidelity.
- Business parameter semantics stay in `MAS-004_RPI-Databridge`.

## Last Reviewed
- Date: 2026-03-04
- Local HEAD baseline during creation: `556c73e`
