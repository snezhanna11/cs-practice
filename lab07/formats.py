import json
import re

_INT = re.compile(r"[-+]?\d+")
_FLOAT = re.compile(r"[-+]?\d+[.,]\d+")

def csv_to_records(text: str) -> list[dict]:
    lines = [line for line in text.lstrip("\ufeff").splitlines() if line.strip()]
    if not lines:
        return []
    header = [h.strip() for h in lines[0].split(",")]
    records = []
    for line in lines[1:]:
        values = [v.strip() for v in line.split(",")]
        values += [""] * (len(header) - len(values))
        records.append(dict(zip(header, values)))
    return records

def _convert(value: str):
    value = value.strip()
    # Заменяем запятую на точку для корректной конвертации чисел с плавающей точкой
    val_normalized = value.replace(",", ".")
    if _INT.fullmatch(val_normalized):
        return int(val_normalized)
    if _FLOAT.fullmatch(val_normalized):
        try:
            return float(val_normalized)
        except ValueError:
            pass
    low = value.lower()
    if low in ("true", "yes"):
        return True
    if low in ("false", "no"):
        return False
    return value

def parse_settings(lines: list[str]) -> dict:
    result = {}
    current_list = None
    for raw in lines:
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if line.startswith("- "):
            if current_list is not None:
                current_list.append(_convert(line[2:].strip()))
            continue
        key, sep, value = line.partition(":")
        if not sep:
            continue
        key, value = key.strip(), value.strip()
        if value == "":
            current_list = []
            result[key] = current_list
        else:
            current_list = None
            result[key] = _convert(value)
    return result

def merge_by_key(rows: list[dict], extra: dict, key: str = "id") -> list[dict]:
    merged = []
    for row in rows:
        info = None
        if key in row:
            value = row[key]
            if value in extra:
                info = extra[value]
            elif str(value) in extra:
                info = extra[str(value)]
        merged.append({**info, **row} if info is not None else dict(row))
    return merged

def records_to_json(records: list[dict]) -> str:
    return json.dumps(records, ensure_ascii=False, indent=2, sort_keys=True)