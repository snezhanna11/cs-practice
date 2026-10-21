from logstats import count_levels, format_report, top_errors


def main():
  filename = input().strip()

  with open(filename, "r", encoding="utf-8") as f:
    counts = count_levels(f)

  with open(filename, "r", encoding="utf-8") as f:
    errors = top_errors(f, 3)

  report_text = format_report(counts, errors)

  with open("report.txt", "w", encoding="utf-8") as f:
    f.write(report_text)


if __name__ == "__main__":
  main()