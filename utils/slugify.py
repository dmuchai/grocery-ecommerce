def slugify_category(name):
    if name is None:
        return ""

    if not isinstance(name, str):
        name = str(name)

    value = name.strip().lower()
    if not value:
        return ""

    return value.replace('&', 'and').replace(' ', '-').replace('--', '-')