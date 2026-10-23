from __future__ import annotations

import ctypes
import os
from pathlib import Path


def local_search_roots() -> tuple[Path, ...]:
    """Gibt lokale feste und wechselbare Laufwerke als Suchwurzeln zurück."""

    if os.name != "nt":
        return (Path("/"),)

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.GetLogicalDrives.restype = ctypes.c_uint32
    kernel32.GetDriveTypeW.argtypes = (ctypes.c_wchar_p,)
    drive_mask = kernel32.GetLogicalDrives()
    roots = []
    for index in range(26):
        if not drive_mask & (1 << index):
            continue
        root = f"{chr(ord('A') + index)}:\\"
        # DRIVE_REMOVABLE=2 and DRIVE_FIXED=3. Network and optical drives
        # can be slow or unavailable, so they are skipped.
        if kernel32.GetDriveTypeW(root) in (2, 3):
            roots.append(Path(root))

    return tuple(roots)


def find_folders_by_name(
    folder_name: str,
    roots: tuple[Path, ...],
    max_results: int = 6,
) -> list[Path]:
    """Sucht einen Ordnernamen unter den angegebenen Laufwerkswurzeln."""

    matches: list[Path] = []
    for root in roots:
        for current, directories, _ in os.walk(root, onerror=lambda _error: None):
            directories[:] = [
                name
                for name in directories
                if not os.path.islink(os.path.join(current, name))
            ]
            for name in directories:
                if name.casefold() == folder_name.casefold():
                    matches.append(Path(current) / name)
                    if len(matches) >= max_results:
                        return matches

    return matches
