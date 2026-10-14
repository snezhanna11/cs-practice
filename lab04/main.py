import sys
from stats import read_valid, parse_record, average_by_city, warmest_city

def main():
    lines = sys.stdin.read().splitlines()
    
    records = read_valid(lines)
    
    errors_count = 0
    for line in lines:
        cleaned = line.strip()
        if not cleaned:
            continue
        try:
            parse_record(cleaned)
        except Exception:
            errors_count += 1

    print(len(records))
    print(errors_count)
    
    if records:
        warm = warmest_city(records)
        averages = average_by_city(records)
        print(averages[warm])
    else:
        print(0.0)

if __name__ == "__main__":
    main()