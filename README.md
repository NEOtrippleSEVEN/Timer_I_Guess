# Space Timer

A simple space-themed timer with:

- **CLI mode** (fast terminal countdown)
- **UI mode** (nice starry window with Start / Pause / Reset)

## Requirements

- Python 3.8+
- Tkinter (usually included with Python)

## Quick Start

### 1) UI mode (recommended)

```bash
python3 space_timer.py --ui
```

In the UI you can:

- Enter a duration (`90` or `01:30`)
- Set a label
- Click **Start**, **Pause**, and **Reset**

### 2) CLI mode

```bash
python3 space_timer.py <duration> [--label "Mission Name"]
```

Examples:

```bash
python3 space_timer.py 30
python3 space_timer.py 01:30
python3 space_timer.py 120 --label "Deep Space Focus"
```

## Duration format

- Seconds: `90`
- Minutes and seconds: `01:30`

## Stop early

- **UI:** click Pause or Reset
- **CLI:** press `Ctrl+C`
