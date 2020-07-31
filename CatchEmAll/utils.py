def nameToFunc(name: str, funcs: []):
    for func in funcs:
        if func.__name__ == name:
            return func
    return None
