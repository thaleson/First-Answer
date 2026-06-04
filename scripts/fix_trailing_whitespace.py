"""Utility script for trimming trailing whitespace from text files."""

import sys
from pathlib import Path


def trim_trailing_whitespace(path: Path) -> bool:
    """Trim trailing whitespace from every line in a file.

    Args:
        path (Path): File path to normalize.

    Returns:
        bool: `True` when the file was modified, otherwise `False`.
    """

    original = path.read_text(encoding="utf-8")
    normalized_lines = [line.rstrip() for line in original.splitlines()]
    normalized = "\n".join(normalized_lines)

    if original.endswith("\n"):
        normalized = f"{normalized}\n"

    if normalized == original:
        return False

    path.write_text(normalized, encoding="utf-8")
    return True


def main() -> int:
    """Run trailing-whitespace normalization for all provided paths.

    Returns:
        int: Exit status indicating whether any file was updated.
    """

    updated = False
    for raw_path in sys.argv[1:]:
        path = Path(raw_path)
        if path.is_file():
            updated = trim_trailing_whitespace(path) or updated

    return 1 if updated else 0


if __name__ == "__main__":
    raise SystemExit(main())
