"""Return whether a Windows PE file has an RT_GROUP_ICON resource."""
from __future__ import annotations

import sys
from pathlib import Path

RT_GROUP_ICON = 14


def pe_has_icon_resource(data: bytes) -> bool:
    try:
        import pefile
    except ImportError:
        return False
    pe = pefile.PE(data=data, fast_load=True)
    pe.parse_data_directories(
        directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_RESOURCE"]]
    )
    if not hasattr(pe, "DIRECTORY_ENTRY_RESOURCE"):
        return False
    for entry in pe.DIRECTORY_ENTRY_RESOURCE.entries:
        if entry.id == RT_GROUP_ICON:
            return True
    return False


def main(argv: list[str] | None = None) -> int:
    path = Path((argv or sys.argv[1:])[0])
    ok = pe_has_icon_resource(path.read_bytes())
    print(f"{path}: icon_resource={'yes' if ok else 'no'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())