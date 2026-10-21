from collections import Counter

def parse_event(line: str) -> dict:
    stripped_line = line.strip()
    if not stripped_line:
        raise ValueError("Пустая строка")
        
    parts = stripped_line.split(maxsplit=2)
    if len(parts) != 3:
        raise ValueError("Неверный формат строки лога")
        
    time_str, level_str, message_str = parts
    
    valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR"}
    if level_str not in valid_levels:
        raise ValueError(f"Неизвестный уровень лога: {level_str}")
        
    return {
        "time": time_str,
        "level": level_str,
        "message": message_str
    }

def count_levels(lines) -> dict:
    counts = {
        "BROKEN": 0,
        "DEBUG": 0,
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0
    }
    
    for line in lines:
        if not line.strip():
            continue
        try:
            event = parse_event(line)
            counts[event["level"]] += 1
        except ValueError:
            counts["BROKEN"] += 1
            
    return counts

def top_errors(lines, n: int) -> list:
    error_messages = []
    
    for line in lines:
        if not line.strip():
            continue
        try:
            event = parse_event(line)
            if event["level"] == "ERROR":
                error_messages.append(event["message"])
        except ValueError:
            continue
            
    counter = Counter(error_messages)
    sorted_errors = sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    
    return [[msg, count] for msg, count in sorted_errors[:n]]

def format_report(counts: dict, errors: list) -> str:
    report_lines = []
    
    for level in sorted(counts.keys()):
        report_lines.append(f"{level}: {counts[level]}")
        
    report_lines.append("")
    report_lines.append("Частые ошибки:")
    
    for err, count in errors:
        report_lines.append(f"- {err} — {count}")
        
    return "\n".join(report_lines) + "\n"