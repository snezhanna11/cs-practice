import sys
from stats import average_by_city, read_valid, warmest_city


def main():
    lines = sys.stdin.read().splitlines()
    records, errors_count = read_valid(lines)
    parsed_count = len(records)

    print(parsed_count)
    print(errors_count)

    if parsed_count > 0:
        best_city = warmest_city(records)
        avg_temps = average_by_city(records)
        print(f"{avg_temps[best_city]:.1f}")
    else:
        print("0.0")


if __name__ == "__main__":
    main()