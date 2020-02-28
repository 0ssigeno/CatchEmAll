import logging as log

import functions
from config import read_main, write_main
from execute_sites import ExecuteSites

LOG_LEVEL = log.INFO
if __name__ == "__main__":
    for handler in log.root.handlers[:]:
        log.root.removeHandler(handler)

    log.basicConfig(format='%(threadName)s %(message)s', level=LOG_LEVEL)

    try:
        LOCAL, MAX_THREADS, MAX_THREADING_FUNCTIONS, MAX_REQ_SAME_PROXY, FUNCTIONS_FILE, PATH_POPULATION = read_main()
        MAX_THREADS = int(MAX_THREADS)
        MAX_THREADING_FUNCTIONS = int(MAX_THREADING_FUNCTIONS)
        MAX_REQ_SAME_PROXY = int(MAX_REQ_SAME_PROXY)
        log.info("Read config file : LOCAL {} , MAX_THREADS {}, MAX_THREADING_FUNCTIONS {}, MAX_REQ_SAME_PROXY {}, "
                 "FUNCTIONS_FILE {}, PATH_POPULATION {}".format(LOCAL, MAX_THREADS, MAX_THREADING_FUNCTIONS,
                                                                MAX_REQ_SAME_PROXY, FUNCTIONS_FILE, PATH_POPULATION))

    except KeyError:
        LOCAL = True
        MAX_THREADS = 1
        MAX_THREADING_FUNCTIONS = 1
        MAX_REQ_SAME_PROXY = 5
        FUNCTIONS_FILE = "functions.py"
        PATH_POPULATION = ""
        write_main(LOCAL, MAX_THREADS, MAX_THREADING_FUNCTIONS, MAX_REQ_SAME_PROXY, FUNCTIONS_FILE, PATH_POPULATION)
        log.info("Wrote config file : LOCAL {} , MAX_THREADS {}, MAX_THREADING_FUNCTIONS {}, MAX_REQ_SAME_PROXY {}, "
                 "FUNCTIONS_FILE {}, PATH_POPULATION {}".format(LOCAL, MAX_THREADS, MAX_THREADING_FUNCTIONS,
                                                                MAX_REQ_SAME_PROXY, FUNCTIONS_FILE, PATH_POPULATION))

    funcs_names = []
    with open(FUNCTIONS_FILE, "r") as f:
        for line in f.readlines():
            if line.startswith("def"):
                funcs_names.append(line.split("(")[0].split(" ")[1])

    functions_to_executes = []
    for func in funcs_names:
        functions_to_executes.append(getattr(functions, func))

    es = ExecuteSites(max_threads_users=MAX_THREADS, max_req_same_proxy=MAX_REQ_SAME_PROXY,
                      max_threading_functions=MAX_THREADING_FUNCTIONS,
                      local=LOCAL)
    if PATH_POPULATION != "":
        log.info("Populating db")
        es.populate_db(PATH_POPULATION)
    es.test_sites(functions_to_executes, funcs_names)
