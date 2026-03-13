from __future__ import annotations

from pathlib import Path
import sys


def _ensure_repo_on_path():
    repo_root = Path(__file__).resolve().parents[1]
    sibling_repo = repo_root.parent / "MAS-004_ZBC-Library"
    package_dir = sibling_repo / "mas004_zbc_library"
    if package_dir.exists():
        sibling_repo_str = str(sibling_repo)
        if sibling_repo_str not in sys.path:
            sys.path.insert(0, sibling_repo_str)


try:
    from mas004_zbc_library import ClarityParameterArchive, MessageId, ZbcClient, dataclass_to_dict, parse_zbc_mapping  # type: ignore[attr-defined]
    from mas004_zbc_library.framing import build_message, parse_message
except ImportError:
    _ensure_repo_on_path()
    from mas004_zbc_library import ClarityParameterArchive, MessageId, ZbcClient, dataclass_to_dict, parse_zbc_mapping  # type: ignore[attr-defined]
    from mas004_zbc_library.framing import build_message, parse_message


__all__ = [
    "ClarityParameterArchive",
    "MessageId",
    "ZbcClient",
    "build_message",
    "dataclass_to_dict",
    "parse_zbc_mapping",
    "parse_message",
]
