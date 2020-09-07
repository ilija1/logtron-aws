def path_get(d, path, default=None):
    keys = path.split(".")
    item = d

    found = True
    for key in keys:
        if key not in item:
            found = False
            break
        item = item[key]

    if found:
        return item, path

    alt_path = path.replace(".", "_")
    if alt_path in d:
        return d[alt_path], alt_path

    return default, None
