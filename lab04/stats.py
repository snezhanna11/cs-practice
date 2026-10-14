def parse_record(line: str) -> dict:
    parts = line.split(";")
    if len(parts) != 3:
        raise ValueError("Строка должна содержать ровно 3 поля")

    city, temp_str, date = parts[0].strip(), parts[1].strip(), parts[2].strip()

    if not city or not date:
        raise ValueError("Поля 'город' и 'дата' не могут быть пустыми")

    try:
        temp = float(temp_str)
    except ValueError:
        raise ValueError("Невозможно преобразовать температуру в число")

    return {"city": city, "temperature": temp, "date": date}


def read_valid(lines: list[str]) -> tuple[list[dict], int]:
    records = []
    errors_count = 0

    for line in lines:
        cleaned_line = line.strip()
        if not cleaned_line:
            continue

        try:
            record = parse_record(cleaned_line)
            records.append(record)
        except Exception:
            errors_count += 1

    return records, errors_count


def average_by_city(records: list[dict]) -> dict:
    city_totals = {}
    city_counts = {}

    for rec in records:
        city = rec["city"]
        temp = rec["temperature"]
        city_totals[city] = city_totals.get(city, 0.0) + temp
        city_counts[city] = city_counts.get(city, 0) + 1

    averages = {}
    for city in city_totals:
        averages[city] = round(city_totals[city] / city_counts[city], 1)

    return averages


def warmest_city(records: list[dict]) -> str:
    if not records:
        return ""

    averages = average_by_city(records)
    sorted_cities = sorted(averages.keys(), key=lambda c: (-averages[c], c))

    return sorted_cities[0]