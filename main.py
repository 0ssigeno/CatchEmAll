import logging as log
from execute_sites import ExecuteSites
import functions
from threading import Thread

log.basicConfig(level=log.INFO, format='%(threadName)s %(message)s')

funcs = []
with open("functions.py", "r") as f:
    for line in f.readlines():
        if line.startswith("def"):
            funcs.append(line.split("(")[0].split(" ")[1])

#es = ExecuteSites(max_threads=1, max_req_same_proxy=3)
#es.db.populate_db("yourPath")
threads = []
for func in funcs:
    method_to_call = getattr(functions, func)
    es = ExecuteSites(max_threads=1, max_req_same_proxy=3)
    es.db.add_column(func)
    thread = Thread(target=es.test_site, args=(method_to_call, func,))
    thread.start()
    log.info("Starting function {}".format(func))
    threads.append(thread)
for t in threads:
    t.join()