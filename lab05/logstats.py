from collections import Counter

VALID_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "D", "I", "W", "E"}
LEVEL_ALIASES = {"D": "DEBUG", "I": "INFO", "W": "WARNING", "E": "ERROR"}

def parse_event(line: str) -> dict:
    line = line.strip()
    if not line:
        raise ValueError("Пустая строка")
    parts = line.split(" ")
    if len(parts) < 2:
        raise ValueError("Недостаточно частей в строке")
    time_str = parts[0]
    level_str = parts[1]
    message_str = " ".join(parts[2:]) if len(parts) > 2 else ""
    if level_str in LEVEL_ALIASES:
        level_str = LEVEL_ALIASES[level_str]
    if level_str not in {"DEBUG", "INFO", "WARNING", "ERROR"}:
        raise ValueError(f"Неизвестный уровень: {level_str}")
    return {"time": time_str, "level": level_str, "message": message_str}

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
            continue
    return counts

def top_errors(lines, limit=3):
    errors = []
    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue
        try:
            event = parse_event(line_str)
            if event["level"] == "ERROR":
                errors.append(event["message"])
        except ValueError:
            continue
    return Counter(errors).most_common(limit)

def format_report(counts, errors):
    lines = ["Отчёт по журналу"]
    for lvl in ["ERROR", "WARNING", "INFO", "DEBUG"]:
        lines.append(f"{lvl}: {counts.get(lvl, 0)}")
    lines.append("Частые ошибки:")
    if not errors:
        lines.append("- нет")
    else:
        for msg, cnt in errors:
            lines.append(f"- {msg} — {cnt}")
    return "\n".join(lines)
