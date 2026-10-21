from collections import Counter


KNOWN_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR"}


def parse_event(line: str) -> dict:
    parts = line.strip().split(maxsplit=2)

    if len(parts) != 3:
        raise ValueError("Некорректная строка журнала")

    timestamp, level, message = parts

    if not timestamp or level not in KNOWN_LEVELS or not message:
        raise ValueError("Некорректная строка журнала")

    return {"time": timestamp, "level": level, "message": message}


def count_levels(lines: list[str]) -> dict:
    """Считает количество строк каждого уровня; плохие строки идут в BROKEN."""
    counts = Counter()

    for line in lines:
        try:
            event = parse_event(line)
        except (ValueError, TypeError, AttributeError):
            counts["BROKEN"] += 1
        else:
            counts[event["level"]] += 1
    return dict(sorted(counts.items()))


def top_errors(lines: list[str], n: int) -> list[list]:
        if n <= 0:
        return []

    errors = Counter()

    for line in lines:
        try:
            event = parse_event(line)
        except (ValueError, TypeError, AttributeError):
            continue

        if event["level"] == "ERROR":
            errors[event["message"]] += 1

    ordered = sorted(errors.items(), key=lambda item: (-item[1], item[0]))
    return [[message, count] for message, count in ordered[:n]]


def format_report(counts: dict, errors: list[list]) -> str:
    result = ["Отчёт по журналу"]

    for level, count in sorted(counts.items()):
        result.append(f"{level}: {count}")

    result.append("")
    result.append("Частые ошибки:")

    for error_desc, count in errors:
        result.append(f"- {error_desc} - {count}")

    return "\n".join(result) + "\n"
