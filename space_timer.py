#!/usr/bin/env python3
"""A simple, dynamic, space-themed countdown timer."""

from __future__ import annotations

import argparse
import itertools
import sys
import time


ORBITAL_FRAMES = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"]
STAR_FRAMES = ["✦", "✧", "⋆", "·"]


class SpaceTimer:
    def __init__(self, total_seconds: int, label: str = "Mission") -> None:
        if total_seconds <= 0:
            raise ValueError("Timer duration must be greater than zero seconds.")
        self.total_seconds = total_seconds
        self.label = label

    @staticmethod
    def _format_time(seconds: int) -> str:
        mins, secs = divmod(seconds, 60)
        hrs, mins = divmod(mins, 60)
        if hrs:
            return f"{hrs:02d}:{mins:02d}:{secs:02d}"
        return f"{mins:02d}:{secs:02d}"

    def run(self) -> None:
        orbit_cycle = itertools.cycle(ORBITAL_FRAMES)
        star_cycle = itertools.cycle(STAR_FRAMES)

        print(f"🚀 {self.label} countdown started: {self._format_time(self.total_seconds)}")
        end = time.time() + self.total_seconds

        while True:
            remaining = max(0, int(round(end - time.time())))
            progress = 1 - (remaining / self.total_seconds)
            bar_length = 24
            filled = int(progress * bar_length)
            bar = "█" * filled + "░" * (bar_length - filled)

            orbit = next(orbit_cycle)
            star = next(star_cycle)
            line = (
                f"\r{orbit} {star} T-{self._format_time(remaining)} "
                f"[{bar}] {int(progress * 100):3d}%"
            )
            print(line, end="", flush=True)

            if remaining == 0:
                break
            time.sleep(0.2)

        print("\n✨ Liftoff! Timer complete. 🌌")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Simple, dynamic, space-themed countdown timer."
    )
    parser.add_argument(
        "duration",
        help="Duration in seconds or mm:ss format (e.g., 90 or 01:30).",
    )
    parser.add_argument(
        "--label",
        default="Mission",
        help="Optional mission label shown on startup.",
    )
    return parser.parse_args()


def parse_duration(value: str) -> int:
    if ":" in value:
        parts = value.split(":")
        if len(parts) != 2 or not all(p.isdigit() for p in parts):
            raise ValueError("Use mm:ss format with numeric values.")
        minutes, seconds = map(int, parts)
        return minutes * 60 + seconds

    if not value.isdigit():
        raise ValueError("Duration must be an integer number of seconds.")
    return int(value)


def main() -> int:
    args = parse_args()
    try:
        duration = parse_duration(args.duration)
        timer = SpaceTimer(duration, args.label)
    except ValueError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1

    try:
        timer.run()
    except KeyboardInterrupt:
        print("\n🛑 Mission aborted by user.")
        return 130
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
