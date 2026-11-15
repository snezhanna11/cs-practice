import os

def count_by_extension(paths: list[str]) -> dict[str, int]:
    result = {}
    for path in paths:
        filename = os.path.basename(path)
        
        
        if '.' in filename and filename.find('.') > 0:
            ext = filename.rsplit('.', 1)[1].lower()
        else:
            ext = ""
            
        result[ext] = result.get(ext, 0) + 1
    return result





def deepest_path(paths: list[str]) -> str:

    if not paths:

        return ""

    return min(paths, key=lambda p: (-p.count("/"), p))





def human_size(n_bytes: int) -> str:

    units = ["Б", "КБ", "МБ", "ГБ", "ТБ"]

    if n_bytes < 1024:

        return f"{n_bytes} Б"

    size = float(n_bytes)

    i = 0

    while size >= 1024 and i < len(units) - 1:

        size /= 1024

        i += 1

    return f"{size:.1f} {units[i]}"