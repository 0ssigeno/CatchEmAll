import functions
from execute_sites import ExecuteSites
import logging as log

MAX_THREADS = 1
MAX_REQ_SAME_PROXY = 5
PATH_POPULATION = None
LOCAL = True
FUNCTIONS_FILE = "functions.py"

if __name__ == "__main__":
    for handler in log.root.handlers[:]:
        log.root.removeHandler(handler)
    log.basicConfig( format='%(threadName)s %(message)s', level=log.INFO)
    funcs_names = []
    with open(FUNCTIONS_FILE, "r") as f:
        for line in f.readlines():
            if line.startswith("def"):
                funcs_names.append(line.split("(")[0].split(" ")[1])

    functions_to_executes = []
    for func in funcs_names:
        functions_to_executes.append(getattr(functions, func))

    es = ExecuteSites(max_threads=MAX_THREADS, max_req_same_proxy=MAX_REQ_SAME_PROXY, threading_sites=False,
                      local=LOCAL)
    if PATH_POPULATION:
        es.populate_db(PATH_POPULATION)
    log.info("Starting with {} threads and changing proxy after {} requests ".format(MAX_THREADS, MAX_REQ_SAME_PROXY))
    es.test_sites(functions_to_executes, funcs_names)
