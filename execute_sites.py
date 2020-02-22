import logging as log
import threading

from Vpn.nordvpn import NordVpn
from manage_db import ManageDb
from manage_requests import ManageRequests


def chunks(seq, num):
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


class ExecuteSites:

    def __init__(self, max_req_same_proxy=5, max_threads=2, threading_sites=False, local=True):
        self.max_req_same_proxy = max_req_same_proxy
        self.max_threads = max_threads
        self.threading_sites = threading_sites
        self.local = local

    def execute_thread(self, nordvpn: NordVpn, users: list, functions_to_execute: list, columns: list):
        """
        function_to_execute is the function that the user define for scrape a single site
        """
        mr = ManageRequests(nordvpn=nordvpn, local=self.local)
        mr.set_random_proxy()
        mr.set_random_user_agent()

        counter_test = 1

        for creds in users:
            usr = creds[0]
            pwd = creds[1]
            if not mr.proxyUsr:
                mr.set_random_proxy()
            if self.threading_sites:
                threads = []
            for j, function_to_execute in enumerate(functions_to_execute):
                mr.db.add_column(columns[j])
                value_user_column = mr.db.retrieve_value_user(usr, pwd, columns[j])
                if value_user_column is None:
                    log.info("Testing {} on site {}".format(usr, columns[j]))
                    counter_test += 1
                    if self.threading_sites:
                        t = threading.Thread(target=function_to_execute, args=(usr, pwd, mr,))
                        threads.append(t)
                    else:
                        function_to_execute(usr, pwd, mr)
                else:
                    log.info("User {} already has a value for {}".format(usr, columns[j]))
                if counter_test == self.max_req_same_proxy:
                    counter_test = 0
                    mr.set_random_proxy()
                    mr.set_random_user_agent()

            if self.threading_sites:
                for t in threads:
                    t.start()
            if self.threading_sites:
                for t in threads:
                    t.join()

    def test_sites(self, functions_to_execute: list, columns: list):
        """
            Create a column for the site that wants to be tested, if is not already present
            Retrieve every users that must be tested
            Divide users in equal parts, each subset will have its own thread
        """
        db = ManageDb(local=self.local)
        users = db.retrieve_all()
        db.close_connection()
        log.info("We are going to test {} users".format(len(users)))
        list_users = chunks(users, self.max_threads)
        threads = []
        nordvpn = NordVpn(request_before_change_server=15)
        log.info("Every thread has {} user".format(len(list_users[0])))
        for users in list_users:
            t = threading.Thread(target=self.execute_thread, args=(nordvpn, users, functions_to_execute, columns,))
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    def populate_db(self, path):
        db = ManageDb(local=self.local)
        db.populate_db(path)
        db.close_connection()
