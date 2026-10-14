import sys
from stats import read_valid, average_by_city, warmest_city

def main():
    lines = sys.stdin.read().splitlines()
    records, errors_count = read_valid(lines)
    
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