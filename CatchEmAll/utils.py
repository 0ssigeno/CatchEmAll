def chunks(seq: list, num: int):
    """
    Should be good to divide the array in equal parts for the threads
    """
    avg = len(seq) / float(num)
    out = []
    last = 0.0
    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    return out


def nameToFunc(name: str, funcs: []):
    for func in funcs:
        if func.__name__ == name:
            return func
    return None
