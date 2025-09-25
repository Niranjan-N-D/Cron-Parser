#!/usr/bin/env python3
import sys

# Define cron field ranges
FIELD_RANGES = {
    "minute": (0, 59),
    "hour": (0, 23),
    "day of month": (1, 31),
    "month": (1, 12),
    "day of week": (0, 6),
}


def expand_field(expr, field):
    start, end = FIELD_RANGES[field]

    # Handle wildcard *
    if expr == "*":
        return list(range(start, end + 1))

    values = set()
    for part in expr.split(","):
        # Step values (e.g. */15)
        if part.startswith("*/"):
            step = int(part[2:])
            values.update(range(start, end + 1, step))
        # Ranges with steps (e.g. 1-10/2)
        elif "-" in part:
            if "/" in part:
                rng, step = part.split("/")
                step = int(step)
                r_start, r_end = map(int, rng.split("-"))
                values.update(range(r_start, r_end + 1, step))
            else:
                r_start, r_end = map(int, part.split("-"))
                values.update(range(r_start, r_end + 1))
        # Single number
        else:
            values.add(int(part))

    return sorted(values)


def parse_cron(cron_str):
    parts = cron_str.strip().split(maxsplit=5)
    if len(parts) < 6:
        raise ValueError("Invalid cron expression, must have 6 parts")

    minute, hour, dom, month, dow, command = parts
    expanded = {
        "minute": expand_field(minute, "minute"),
        "hour": expand_field(hour, "hour"),
        "day of month": expand_field(dom, "day of month"),
        "month": expand_field(month, "month"),
        "day of week": expand_field(dow, "day of week"),
        "command": command,
    }
    return expanded


def format_output(expanded):
    for field in ["minute", "hour", "day of month", "month", "day of week"]:
        print(f"{field:<14}{' '.join(map(str, expanded[field]))}")
    print(f"{'command':<14}{expanded['command']}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: cron_parser.py \"<cron expression>\"")
        sys.exit(1)

    cron_str = sys.argv[1]
    expanded = parse_cron(cron_str)
    format_output(expanded)
