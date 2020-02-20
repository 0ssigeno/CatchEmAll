import logging as log

import functions
from execute_sites import ExecuteSites

MAX_THREADS = 1
MAX_REQ_SAME_PROXY = 5
PATH_POPULATION = "./test"

if __name__ == "__main__":
    log.basicConfig(level=log.INFO, format='%(threadName)s %(message)s')

    funcs_names = []
    with open("functions.py", "r") as f:
        for line in f.readlines():
            if line.startswith("def"):
                funcs_names.append(line.split("(")[0].split(" ")[1])

    functions_to_executes = []
    for func in funcs_names:
        functions_to_executes.append(getattr(functions, func))

    es = ExecuteSites(max_threads=MAX_THREADS, max_req_same_proxy=MAX_REQ_SAME_PROXY, threading_sites=False)
    if PATH_POPULATION:
        es.db.populate_db(PATH_POPULATION)
    log.info("Starting with {} threads and changing proxy after {} requests ".format(MAX_THREADS, MAX_REQ_SAME_PROXY))
    es.test_site(functions_to_executes, funcs_names)
