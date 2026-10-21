from collections import Counter

def count_levels(log_lines):
    levels = []
    for line in log_lines:
        parts = line.split()
        if len(parts) >= 2:
            level = parts[1]
            levels.append(level)
    return dict(Counter(levels))

def format_report(level_counts, top_errors):
    result = ["Отчёт по журналу", ""]
    
    for level, count in level_counts.items():
        result.append(f"{level}: {count}")
        
    result.append("Частые ошибки:")
    
    for error_desc, count in top_errors:
        result.append(f"- {error_desc} – {count}")
        
    return "\n".join(result) + "\n"

def process_log_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        return lines
    except FileNotFoundError:
        return []