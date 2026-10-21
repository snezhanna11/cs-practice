VALID_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR"}


def parse_event(line: str) -> dict:
    line = line.strip()
    if not line:
        raise ValueError("Пустая строка")

    parts = line.split(" ", 2)
    if len(parts) < 3:
        raise ValueError("Недостаточно частей в строке")

    time_str, level_str, message_str = parts

    if level_str not in VALID_LEVELS:
        raise ValueError(f"Неизвестный уровень: {level_str}")

    return {
        "time": time_str,
        "level": level_str,
        "message": message_str,
    }


def count_levels(lines) -> dict:
    counts = {}

    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue

        try:
            event = parse_event(line_str)
            lvl = event["level"]
            counts[lvl] = counts.get(lvl, 0) + 1
        except ValueError:
            counts["BROKEN"] = counts.get("BROKEN", 0) + 1

    return counts


def top_errors(lines, n: int) -> list:
    error_counts = {}

    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue

        try:
            event = parse_event(line_str)
            if event["level"] == "ERROR":
                msg = event["message"]
                error_counts[msg] = error_counts.get(msg, 0) + 1
        except ValueError:
            pass

    sorted_errors = sorted(
        error_counts.items(), key=lambda item: (-item[1], item[0])
    )

    return [[msg, count] for msg, count in sorted_errors[:n]]


def format_report(counts: dict, errors: list) -> str:
    lines_out = ["Отчёт по журналу", ""]

    for level in sorted(counts.keys()):
        lines_out.append(f"{level}: {counts[level]}")

    lines_out.append("")
    lines_out.append("Частые ошибки:")

    for msg, count in errors:
        lines_out.append(f"- {msg} - {count}")

    return "\n".join(lines_out) + "\n"