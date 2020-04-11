def find_items_starting_with(string, items):
    return [i for i, line in enumerate(items) if line.startswith(string)]
