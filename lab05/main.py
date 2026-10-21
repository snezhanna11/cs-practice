from logstats import parse_event, count_levels, top_errors, format_report


def main():
    filename = input().strip()

    total_lines = 0
    error_lines = 0
    broken_lines = 0
    counts = {}
    errors = []

    try:
        with open(filename, "r", encoding="utf-8") as log:
            for line in log:
                line = line.strip()
                if not line:
                    continue

                total_lines += 1
                try:
                    event = parse_event(line)
                except ValueError:
                    broken_lines += 1
                else:
                    if event["level"] == "ERROR":
                        error_lines += 1
        with open(filename, "r", encoding="utf-8") as log:
            counts = {}
            error_messages = []
            from collections import Counter
            level_counter = Counter()
            error_counter = Counter()

            for line in log:
                line = line.strip()
                if not line:
                    continue
                try:
                    event = parse_event(line)
                except ValueError:
                    level_counter["BROKEN"] += 1
                    continue

                level_counter[event["level"]] += 1
                if event["level"] == "ERROR":
                    error_counter[event["message"]] += 1

            counts = dict(sorted(level_counter.items()))
            errors = [
                [message, count]
                for message, count in sorted(
                    error_counter.items(), key=lambda item: (-item[1], item[0])
                )[:3]
            ]

        report = format_report(counts, errors)
        with open("report.txt", "w", encoding="utf-8") as report_file:
            report_file.write(report)

        print(total_lines)
        print(error_lines)
        print(broken_lines)

    except OSError:
        print(0)
        print(0)
        print(0)


if __name__ == "__main__":
    main()
