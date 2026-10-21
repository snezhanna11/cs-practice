from logstats import count_levels, top_errors, format_report

def main():
    try:
        log_filename = input().strip()
    except EOFError:
        return

    with open(log_filename, "r", encoding="utf-8") as log_file:
        counts = count_levels(log_file)
        
    total_lines = sum(counts.values())
    error_count = counts.get("ERROR", 0)
    broken_count = counts.get("BROKEN", 0)

    print(total_lines)
    print(error_count)
    print(broken_count)

    with open(log_filename, "r", encoding="utf-8") as log_file:
        errors = top_errors(log_file, n=3)

    report_text = format_report(counts, errors)

    with open("report.txt", "w", encoding="utf-8") as report_file:
        report_file.write(report_text)

if __name__ == "__main__":
    main()