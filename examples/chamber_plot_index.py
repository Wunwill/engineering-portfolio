"""Portfolio demonstration using synthetic paths, not CERN production code.

Indexes chamber-specific PNG paths. Does not open images or perform physics
analysis. Aggregate wheel/station maps are outside this example's scope.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path, PurePosixPath
import re
from typing import Iterable


@dataclass(frozen=True, order=True)
class Chamber:
    wheel: int
    station: int
    sector: int

    def __post_init__(self) -> None:
        if self.wheel not in range(-2, 3):
            raise ValueError("Wheel must be between -2 and 2.")
        if self.station not in range(1, 5):
            raise ValueError("Station must be between 1 and 4.")
        limit = 14 if self.station == 4 else 12
        if self.sector not in range(1, limit + 1):
            raise ValueError(f"Station {self.station} sectors must be 1-{limit}.")


def parse_plot_path(value: str) -> tuple[Chamber, str]:
    """Accept relative wheel/station/sector/file paths, not absolute paths."""
    if not isinstance(value, str):
        raise ValueError("Each plot path must be a string.")
    normalized = value.replace("\\", "/")
    parts = normalized.split("/")
    if len(parts) != 4 or any(part in ("", ".", "..") for part in parts):
        raise ValueError(f"Expected wheel/station/sector/file.png: {value!r}")
    wheel_match = re.fullmatch(r"MB([+-][0-2])", parts[0])
    if wheel_match is None or parts[1] not in ("1", "2", "3", "4"):
        raise ValueError(f"Invalid wheel or station: {value!r}")
    if re.fullmatch(r"[0-9]{2}", parts[2]) is None:
        raise ValueError(f"Sector must use two digits: {value!r}")
    if re.fullmatch(r"[A-Za-z0-9_-]+\.png", parts[3]) is None:
        raise ValueError(f"Expected a simple PNG filename: {value!r}")
    chamber = Chamber(int(wheel_match.group(1)), int(parts[1]), int(parts[2]))
    return chamber, PurePosixPath(*parts).as_posix()


def build_index(paths: Iterable[str]) -> dict[Chamber, tuple[str, ...]]:
    """Deduplicate paths and return a deterministic chamber-to-plots mapping."""
    grouped: dict[Chamber, set[str]] = {}
    for value in paths:
        chamber, path = parse_plot_path(value)
        grouped.setdefault(chamber, set()).add(path)
    return {chamber: tuple(sorted(grouped[chamber])) for chamber in sorted(grouped)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="JSON array of relative PNG paths")
    parser.add_argument("--wheel", required=True, type=int)
    parser.add_argument("--station", required=True, type=int)
    parser.add_argument("--sector", required=True, type=int)
    args = parser.parse_args()
    try:
        selection = Chamber(args.wheel, args.station, args.sector)
        paths = json.loads(args.manifest.read_text(encoding="utf-8"))
        if not isinstance(paths, list):
            raise ValueError("Manifest must be a JSON array of path strings.")
        index = build_index(paths)
    except (OSError, ValueError) as error:
        parser.exit(2, f"error: {error}\n")
    print(json.dumps(index.get(selection, ()), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
