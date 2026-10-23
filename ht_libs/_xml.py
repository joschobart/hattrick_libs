"""Small XML helpers shared by the parsers."""


def optional_text(tag, *names, default=""):
    """Text of the first child found under any of `names`, else `default`.

    For tags CHPP only sends in some file versions or for some teams.
    """
    if tag is None:
        return default
    for name in names:
        found = tag.find(name)
        if found is not None and found.contents:
            return found.contents[0]
    return default
