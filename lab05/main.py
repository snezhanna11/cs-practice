from logstats import count_levels, format_report, parse_event, top_errors


def main():
    filename = "events"

    total_parsed = 0
    error_count = 0
    broken_count = 0

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if not line_str:
                continue

            try:
                event = parse_event(line_str)
                total_parsed += 1
                if event["level"] == "ERROR":
                    error_count += 1
            except ValueError:
                broken_count += 1

    print(total_parsed)
    print(error_count)
    print(broken_count)

    with open(filename, "r", encoding="utf-8") as f:
        counts = count_levels(f)

    with open(filename, "r", encoding="utf-8") as f:
        errors = top_errors(f, 3)

    report_text = format_report(counts, errors)

    with open("report.txt", "w", encoding="utf-8") as f:
        f.write(report_text)


if __name__ == "__main__":
    main()
