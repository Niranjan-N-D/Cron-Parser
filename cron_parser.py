#!/usr/bin/env python3
import sys

# Allowed ranges for each cron field
CRON_LIMITS = {
    "minute": (0, 59),
    "hour": (0, 23),
    "day": (1, 31),
    "month": (1, 12),
    "weekday": (0, 6),
}


def expand_cron_field(field_expr, field_name):
    """Expand a cron field like */5 or 1-10 into a list of numbers."""
    start, end = CRON_LIMITS[field_name]

    if field_expr == "*":
        return list(range(start, end + 1))

    result = set()
    for part in field_expr.split(","):
        if part.startswith("*/"):  # step values
            step = int(part[2:])
            result.update(range(start, end + 1, step))
        elif "-" in part:  # range or range with step
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

    return sorted(result)


def parse_cron_expr(expr):
    fields = expr.strip().split(maxsplit=5)
    if len(fields) < 6:
        raise ValueError("Cron expression must have 6 parts")

    minute, hour, day, month, weekday, command = fields
    return {
        "minute": expand_cron_field(minute, "minute"),
        "hour": expand_cron_field(hour, "hour"),
        "day": expand_cron_field(day, "day"),
        "month": expand_cron_field(month, "month"),
        "weekday": expand_cron_field(weekday, "weekday"),
        "command": command,
    }


def show_schedule(schedule):
    """Print expanded cron schedule in readable format."""
    print(f"{'minute':<10}{' '.join(map(str, schedule['minute']))}")
    print(f"{'hour':<10}{' '.join(map(str, schedule['hour']))}")
    print(f"{'day':<10}{' '.join(map(str, schedule['day']))}")
    print(f"{'month':<10}{' '.join(map(str, schedule['month']))}")
    print(f"{'weekday':<10}{' '.join(map(str, schedule['weekday']))}")
    print(f"{'command':<10}{schedule['command']}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python cron_parser.py \"<cron expression>\"")
        sys.exit(1)

    cron_expr = sys.argv[1]
    schedule = parse_cron_expr(cron_expr)
    show_schedule(schedule)
