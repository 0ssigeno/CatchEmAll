import logging as log
from execute_sites import ExecuteSites
import functions

log.basicConfig(level=log.INFO, format='%(threadName)s %(message)s')

funcs=[]
with open("functions.py","r") as f:
    for line in f.readlines():
        if line.startswith("def"):
            funcs.append(line.split("(")[0].split(" ")[1])

es = ExecuteSites(max_threads=1, max_req_same_proxy=3)

es.db.populate_db("/home/methk/Documents/Shady/CatchEmAll/test")
#es.db.add_column("spotify")
#es.db.add_column("nordvpnProxy")
#
for func in funcs:
    method_to_call = getattr(functions, func)
    es.db.add_column(func)
    es.test_site(method_to_call, func)