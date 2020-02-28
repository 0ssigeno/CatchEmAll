import logging as log

from config import read_main, write_main
from execute_sites import ExecuteSites

LOG_LEVEL = log.INFO


def main():
    for handler in log.root.handlers[:]:
        log.root.removeHandler(handler)

    log.basicConfig(format='%(threadName)s %(message)s', level=LOG_LEVEL)

    try:
        local, max_threads, max_threading_functions, max_req_same_proxy, pokedex, path_population = read_main()
        max_threads = int(max_threads)
        max_threading_functions = int(max_threading_functions)
        max_req_same_proxy = int(max_req_same_proxy)
        log.info("Read config file : local {} , max_threads {}, max_threading_functions {}, max_req_same_proxy {}, "
                 "pokedex {}, path_population {}".format(local, max_threads, max_threading_functions,
                                                         max_req_same_proxy, pokedex, path_population))

    except KeyError:
        local = True
        max_threads = 1
        max_threading_functions = 1
        max_req_same_proxy = 5
        pokedex = "PokedexOwned"
        path_population = ""
        write_main(local, max_threads, max_threading_functions, max_req_same_proxy, pokedex, path_population)
        log.info("Wrote config file : local {} , max_threads {}, max_threading_functions {}, max_req_same_proxy {}, "
                 "pokedex {}, path_population {}".format(local, max_threads, max_threading_functions,
                                                         max_req_same_proxy, pokedex, path_population))

    funcs = dynamic_loader(pokedex)
    funcs_names = list(funcs.keys())
    functions_to_executes = list(funcs.values())
    print(funcs_names)
    print(functions_to_executes)
    es = ExecuteSites(max_threads_users=max_threads, max_req_same_proxy=max_req_same_proxy,
                      max_threading_functions=max_threading_functions,
                      local=local)
    if path_population != "":
        log.info("Populating db")
        es.populate_db(path_population)
    es.test_sites(functions_to_executes, funcs_names)


def dynamic_loader(path):
    functions = {}
    import os
    lst = os.listdir(path)
    lst = [elem for elem in lst if elem.endswith(".py")]
    for f in lst:
        f = os.path.splitext(f)[0]
        module = __import__(path + "." + f, fromlist=["*"])
        functions[f] = getattr(module, f)
    return functions


if __name__ == "__main__":
    main()
