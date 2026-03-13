from __future__ import annotations

import struct
from datetime import date, datetime
from dataclasses import dataclass
import time
from typing import Any

from .mapper import ZbcMapping, decode_value, encode_value
from ._zbc_library import ClarityParameterArchive, MessageId, ZbcClient, build_message, dataclass_to_dict, parse_message


@dataclass(frozen=True)
class ProbeResult:
    profile_name: str
    machine_name: str
    machine_model: str
    job_name: str
    ribbon_level: str | None
    active_faults: tuple[str, ...]
    active_warnings: tuple[str, ...]


class ZbcBridgeClient:
    """Bridge-facing wrapper around the shared MAS-004 ZBC library."""

    def __init__(self, host: str, port: int, timeout_s: float = 8.0, retry_count: int = 3, retry_delay_s: float = 1.0):
        self.host = (host or "").strip()
        self.port = int(port or 0)
        self.timeout_s = float(timeout_s)
        self.retry_count = max(1, int(retry_count))
        self.retry_delay_s = max(0.0, float(retry_delay_s))

    def write(self, mapping: ZbcMapping, value: str) -> tuple[int, bytes]:
        body = struct.pack("<H", mapping.command_id & 0xFFFF) + encode_value(value, mapping.codec, mapping.scale, mapping.offset)
        return self.transact(mapping.message_id, body)

    def read(self, mapping: ZbcMapping) -> str:
        body = struct.pack("<H", mapping.command_id & 0xFFFF)
        msg_id, payload = self.transact(mapping.message_id, body)
        if len(payload) >= 2 and struct.unpack("<H", payload[:2])[0] == (mapping.command_id & 0xFFFF):
            payload = payload[2:]
        return decode_value(payload, mapping.codec, mapping.scale, mapping.offset)

    def transact(self, message_id: int, body: bytes = b"") -> tuple[int, bytes]:
        if not self.host or self.port <= 0:
            raise RuntimeError("host/port not configured")
        return self._with_client(lambda client: parse_message(client._ensure_transport().exchange_message(build_message(message_id, body))), retries=1)

    def probe(self) -> ProbeResult:
        def _collect(client: ZbcClient):
            profile = client.detect_profile()
            summary = client.request_summary_info()
            return profile, dataclass_to_dict(summary)

        profile, data = self._with_client(_collect)
        tags = {tag["name"]: tag["value"] for tag in data.get("tags", [])}
        machine = tags.get("mch") or {}
        job = tags.get("jin") or {}
        lei = tags.get("lei") or {}
        supplies = tags.get("sup") or {}
        ribbon_level = None
        for consumable in supplies.get("consumables", []):
            if consumable.get("type") == "Ribbon":
                ribbon_level = consumable.get("level")
                break
        return ProbeResult(
            profile_name=profile.name,
            machine_name=str(machine.get("name") or ""),
            machine_model=str(machine.get("model") or ""),
            job_name=str(job.get("name") or ""),
            ribbon_level=ribbon_level,
            active_faults=tuple(entry.get("name", "") for entry in lei.get("faults", [])),
            active_warnings=tuple(entry.get("name", "") for entry in lei.get("warnings", [])),
        )

    def request_current_parameters(self) -> ClarityParameterArchive:
        return self._with_client(lambda client: client.request_current_parameters())

    def read_current_parameter(self, path: str) -> str | None:
        leaf = self.request_current_parameters().find_by_path(path)
        return leaf.value if leaf is not None else None

    def write_current_parameters(self, archive: ClarityParameterArchive | bytes | bytearray | str, file_name: str = "CurrentParameters.xml") -> tuple[int, Any]:
        return self._with_client(lambda client: client.write_current_parameters(archive, file_name=file_name))

    def write_current_parameter(self, path: str, value: str | int | float | bool, verify_readback: bool = True) -> tuple[int, str | None]:
        def _write(client: ZbcClient):
            message_id, _response = client.update_current_parameter(path, value)
            verified = None
            if verify_readback and message_id == MessageId.NUL:
                verified_leaf = client.request_current_parameters().find_by_path(path)
                verified = verified_leaf.value if verified_leaf is not None else None
            return message_id, verified
        return self._with_client(_write)

    def summary_dict(self) -> dict[str, Any]:
        def _summary(client: ZbcClient):
            profile = client.detect_profile()
            summary = client.request_summary_info()
            return profile, summary
        profile, summary = self._with_client(_summary)
        return {
            "profile": profile.name,
            "summary": _json_safe(dataclass_to_dict(summary)),
        }

    def _open_client(self) -> ZbcClient:
        return ZbcClient(self.host, self.port, timeout_s=self.timeout_s)

    def _with_client(self, fn, retries: int | None = None):
        attempts = retries if retries is not None else self.retry_count
        last_error = None
        for attempt in range(1, attempts + 1):
            try:
                with self._open_client() as client:
                    return fn(client)
            except Exception as exc:
                last_error = exc
                if attempt >= attempts:
                    raise
                time.sleep(self.retry_delay_s)
        raise last_error  # pragma: no cover


def _json_safe(value: Any) -> Any:
    if isinstance(value, bytes):
        return value.hex()
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    return value
