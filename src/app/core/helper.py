def remove_duplicates(lst):
    seen = set()
    result = []
    for item in lst:
        if item.id not in seen:
            result.append(item)
            seen.add(item.id)
    return result