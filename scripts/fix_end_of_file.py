"""Utility script for ensuring files end with a single trailing newline."""

import sys
from pathlib import Path


def normalize_end_of_file(path: Path) -> bool:
    """Normalize the final newline of a file.

    Args:
        path (Path): File path to normalize.

    Returns:
        bool: `True` when the file was modified, otherwise `False`.
    """

    original = path.read_bytes()
    if not original:
        return False

    normalized = original.rstrip(b"\n") + b"\n"
    if normalized == original:
        return False

    path.write_bytes(normalized)
    return True


def main() -> int:
    """Run the end-of-file normalization for all provided paths.

    Returns:
        int: Exit status indicating whether any file was updated.
    """

    updated = False
    for raw_path in sys.argv[1:]:
        path = Path(raw_path)
        if path.is_file():
            updated = normalize_end_of_file(path) or updated

    return 1 if updated else 0


if __name__ == "__main__":
    raise SystemExit(main())
