#!/usr/bin/env python3
"""A simple, dynamic, space-themed countdown timer (CLI + UI)."""

from __future__ import annotations

import argparse
import itertools
import random
import sys
import time
import tkinter as tk
from tkinter import ttk


ORBITAL_FRAMES = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"]
STAR_FRAMES = ["✦", "✧", "⋆", "·"]


class SpaceTimer:
    def __init__(self, total_seconds: int, label: str = "Mission") -> None:
        if total_seconds <= 0:
            raise ValueError("Timer duration must be greater than zero seconds.")
        self.total_seconds = total_seconds
        self.label = label

    @staticmethod
    def format_time(seconds: int) -> str:
        mins, secs = divmod(seconds, 60)
        hrs, mins = divmod(mins, 60)
        if hrs:
            return f"{hrs:02d}:{mins:02d}:{secs:02d}"
        return f"{mins:02d}:{secs:02d}"

    def run_cli(self) -> None:
        orbit_cycle = itertools.cycle(ORBITAL_FRAMES)
        star_cycle = itertools.cycle(STAR_FRAMES)

        print(f"🚀 {self.label} countdown started: {self.format_time(self.total_seconds)}")
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
                f"\r{orbit} {star} T-{self.format_time(remaining)} "
                f"[{bar}] {int(progress * 100):3d}%"
            )
            print(line, end="", flush=True)

            if remaining == 0:
                break
            time.sleep(0.2)

        print("\n✨ Liftoff! Timer complete. 🌌")


class SpaceTimerUI:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Space Timer")
        self.root.geometry("520x420")
        self.root.configure(bg="#090B1A")

        self.total_seconds = 0
        self.remaining = 0
        self.running = False
        self.end_time = 0.0
        self.star_items: list[int] = []
        self.star_alphas: list[int] = []

        self._build_ui()
        self._seed_stars()
        self._animate_stars()

    def _build_ui(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Space.TFrame", background="#090B1A")
        style.configure("Space.TLabel", background="#090B1A", foreground="#DDE8FF")

        container = ttk.Frame(self.root, style="Space.TFrame", padding=16)
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            container,
            height=150,
            bg="#11142A",
            highlightthickness=0,
            bd=0,
        )
        self.canvas.pack(fill="x")

        title = ttk.Label(
            container,
            text="🌌 Space Timer",
            style="Space.TLabel",
            font=("TkDefaultFont", 17, "bold"),
        )
        title.pack(pady=(14, 8))

        self.time_var = tk.StringVar(value="00:00")
        self.time_label = ttk.Label(
            container,
            textvariable=self.time_var,
            style="Space.TLabel",
            font=("TkDefaultFont", 36, "bold"),
        )
        self.time_label.pack(pady=(0, 8))

        inputs = ttk.Frame(container, style="Space.TFrame")
        inputs.pack(fill="x", pady=6)

        ttk.Label(inputs, text="Duration (seconds or mm:ss)", style="Space.TLabel").pack(
            anchor="w"
        )
        self.duration_entry = tk.Entry(
            inputs,
            bg="#1C2140",
            fg="#F0F6FF",
            insertbackground="#F0F6FF",
            relief="flat",
            font=("TkDefaultFont", 12),
        )
        self.duration_entry.pack(fill="x", pady=(4, 10), ipady=6)
        self.duration_entry.insert(0, "01:00")

        ttk.Label(inputs, text="Label", style="Space.TLabel").pack(anchor="w")
        self.label_entry = tk.Entry(
            inputs,
            bg="#1C2140",
            fg="#F0F6FF",
            insertbackground="#F0F6FF",
            relief="flat",
            font=("TkDefaultFont", 12),
        )
        self.label_entry.pack(fill="x", pady=(4, 12), ipady=6)
        self.label_entry.insert(0, "Mission")

        self.progress = ttk.Progressbar(container, maximum=100, value=0)
        self.progress.pack(fill="x", pady=(4, 12))

        button_row = ttk.Frame(container, style="Space.TFrame")
        button_row.pack(fill="x", pady=(2, 4))

        self.start_button = tk.Button(
            button_row,
            text="Start",
            command=self.start_timer,
            bg="#2D62FF",
            fg="white",
            relief="flat",
            padx=14,
            pady=8,
        )
        self.start_button.pack(side="left", padx=(0, 8))

        self.pause_button = tk.Button(
            button_row,
            text="Pause",
            command=self.pause_timer,
            bg="#3A4062",
            fg="white",
            relief="flat",
            padx=14,
            pady=8,
        )
        self.pause_button.pack(side="left", padx=(0, 8))

        self.reset_button = tk.Button(
            button_row,
            text="Reset",
            command=self.reset_timer,
            bg="#3A4062",
            fg="white",
            relief="flat",
            padx=14,
            pady=8,
        )
        self.reset_button.pack(side="left")

        self.status_var = tk.StringVar(value="Ready for launch 🚀")
        status_label = ttk.Label(container, textvariable=self.status_var, style="Space.TLabel")
        status_label.pack(anchor="w", pady=(10, 0))

    def _seed_stars(self) -> None:
        width, height = 520, 150
        for _ in range(65):
            x = random.randint(8, width - 8)
            y = random.randint(8, height - 8)
            size = random.choice((2, 3))
            alpha = random.randint(130, 255)
            color = self._star_color(alpha)
            star = self.canvas.create_oval(x, y, x + size, y + size, fill=color, outline=color)
            self.star_items.append(star)
            self.star_alphas.append(alpha)

    @staticmethod
    def _star_color(alpha: int) -> str:
        shade = max(110, min(255, alpha))
        return f"#{shade:02x}{shade:02x}ff"

    def _animate_stars(self) -> None:
        for idx, star in enumerate(self.star_items):
            delta = random.randint(-20, 20)
            self.star_alphas[idx] = max(110, min(255, self.star_alphas[idx] + delta))
            color = self._star_color(self.star_alphas[idx])
            self.canvas.itemconfig(star, fill=color, outline=color)
        self.root.after(240, self._animate_stars)

    def _set_from_input(self) -> bool:
        try:
            seconds = parse_duration(self.duration_entry.get().strip())
            if seconds <= 0:
                raise ValueError("Duration must be greater than zero.")
        except ValueError as err:
            self.status_var.set(f"⚠️ {err}")
            return False

        self.total_seconds = seconds
        self.remaining = seconds
        self.time_var.set(SpaceTimer.format_time(self.remaining))
        self.progress.configure(value=0)
        return True

    def start_timer(self) -> None:
        if self.running:
            return

        if self.remaining <= 0:
            if not self._set_from_input():
                return

        self.running = True
        self.end_time = time.time() + self.remaining
        self.status_var.set(f"🛰️ {self.label_entry.get().strip() or 'Mission'} in progress")
        self._tick()

    def pause_timer(self) -> None:
        if not self.running:
            return
        self.running = False
        self.remaining = max(0, int(round(self.end_time - time.time())))
        self.time_var.set(SpaceTimer.format_time(self.remaining))
        self.status_var.set("⏸️ Paused")

    def reset_timer(self) -> None:
        self.running = False
        if self._set_from_input():
            self.status_var.set("Ready for launch 🚀")

    def _tick(self) -> None:
        if not self.running:
            return

        self.remaining = max(0, int(round(self.end_time - time.time())))
        self.time_var.set(SpaceTimer.format_time(self.remaining))

        if self.total_seconds > 0:
            done = (self.total_seconds - self.remaining) / self.total_seconds
            self.progress.configure(value=int(done * 100))

        if self.remaining == 0:
            self.running = False
            self.status_var.set("✨ Liftoff! Timer complete.")
            return

        self.root.after(150, self._tick)

    def run(self) -> None:
        self.root.mainloop()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Simple, dynamic, space-themed countdown timer."
    )
    parser.add_argument(
        "duration",
        nargs="?",
        help="Duration in seconds or mm:ss format (e.g., 90 or 01:30).",
    )
    parser.add_argument(
        "--label",
        default="Mission",
        help="Optional mission label shown on startup (CLI mode).",
    )
    parser.add_argument(
        "--ui",
        action="store_true",
        help="Launch the graphical space timer UI.",
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

    if args.ui:
        app = SpaceTimerUI()
        app.run()
        return 0

    if not args.duration:
        print("Error: duration is required in CLI mode unless --ui is used.", file=sys.stderr)
        return 2

    try:
        duration = parse_duration(args.duration)
        timer = SpaceTimer(duration, args.label)
    except ValueError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1

    try:
        timer.run_cli()
    except KeyboardInterrupt:
        print("\n🛑 Mission aborted by user.")
        return 130
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
