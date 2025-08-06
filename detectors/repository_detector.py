def is_repository_class(ts_class) -> bool:
    # Accept if class name ends with Repository (case-insensitive)
    if ts_class.name.lower().endswith("repository"):
        return True

    # Accept if class has decorator 'repository'
    if any(d.name.lower() == "repository" for d in ts_class.decorators):
        return True

    return False
