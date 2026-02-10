# Space Timer

A simple, straightforward, space-themed countdown timer for the terminal.

## Requirements

- Python 3.8+

## Run

```bash
python3 space_timer.py <duration> [--label "Mission Name"]
```

## Duration formats

You can pass duration as:

- Seconds: `90`
- Minutes and seconds: `01:30`

## Examples

```bash
python3 space_timer.py 30
python3 space_timer.py 01:30
python3 space_timer.py 120 --label "Deep Space Focus"
```

## What it shows

- A countdown (`T-00:30`)
- A subtle animated moon/star indicator
- A progress bar and percentage

## Stop early

Press `Ctrl+C` to cancel the timer.
