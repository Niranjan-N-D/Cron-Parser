#!/usr/bin/env python3
import sys

# Cron field limits
CRON_LIMITS = {
    "minute": (0, 59),
    "hour": (0, 23),
    "day of month": (1, 31),
    "month": (1, 12),
    "day of week": (0, 6),
}


def expand_cron_field(field_expr, field_name):
    """Turn a cron field into a list of valid numbers."""
    start, end = CRON_LIMITS[field_name]

    if field_expr == "*":
        return list(range(start, end + 1))

    result = set()
    for part in field_expr.split(","):
        if part.startswith("*/"):  # step like */15
            step = int(part[2:])
            result.update(range(start, end + 1, step))
        elif "-" in part:  # range (with or without step)
            if "/" in part:
                rng, step = part.split("/")
                step = int(step)
                r_start, r_end = map(int, rng.split("-"))
                result.update(range(r_start, r_end + 1, step))
            else:
                r_start, r_end = map(int, part.split("-"))
                result.update(range(r_start, r_end + 1))
        else:  # single value
            result.add(int(part))

    # ✅ Validate numbers are within allowed limits
    for val in result:
        if val < start or val > end:
            raise ValueError(
                f"Invalid value {val} for '{field_name}'. Allowed range: {start}-{end}"
            )

    return sorted(result)


def parse_cron_expr(cron_expr):
    """Split and expand cron expression into fields."""
    parts = cron_expr.strip().split(maxsplit=5)
    if len(parts) < 6:
        raise ValueError("Cron expression must have 6 parts")

    minute, hour, dom, month, dow, command = parts
    return {
        "minute": expand_cron_field(minute, "minute"),
        "hour": expand_cron_field(hour, "hour"),
        "day of month": expand_cron_field(dom, "day of month"),
        "month": expand_cron_field(month, "month"),
        "day of week": expand_cron_field(dow, "day of week"),
        "command": command,
    }


def show_schedule(expanded):
    """Print results in a nice table."""
    for field in ["minute", "hour", "day of month", "month", "day of week"]:
        print(f"{field:<14}{' '.join(map(str, expanded[field]))}")
    print(f"{'command':<14}{expanded['command']}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python cron_parser.py \"<cron expression>\"")
        sys.exit(1)

    try:
        expanded = parse_cron_expr(sys.argv[1])
        show_schedule(expanded)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
