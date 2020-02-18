import logging as log
from manage_requests import ManageRequests
import threading
from manage_db import ManageDb


class ExecuteSites:

    def __init__(self, max_req_same_proxy=5, max_threads=2):
        self.max_req_same_proxy = max_req_same_proxy
        self.max_threads = max_threads
        self.db = ManageDb()

    def chunks(self, seq, num):
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

    def execute_thread(self, users, function_to_execute):
        """
        function_to_execute is the function that the user define for scrape a single site
        """
        mr = ManageRequests()
        for i, creds in enumerate(users):
            usr = creds[0]
            pwd = creds[1]
            if i % self.max_req_same_proxy == 0:
                mr.set_random_proxy()
                mr.set_random_user_agent()
            if not mr.proxyUsr:
                mr.set_random_proxy()

            function_to_execute(usr, pwd, mr)

    def test_site(self, function_to_execute, column):
        """
            Create a column for the site that wants to be tested, if is not already present
            Retrieve every users that must be tested
            Divide users in equal parts, each subset will have its own thread
        """
        self.db.add_column(column)
        users = self.db.retrieve_users(column, "NULL")
        log.info("We are going to test {} users".format(len(users)))
        list_users = self.chunks(users, self.max_threads)
        threads = []
        for users in list_users:
            log.info("Starting thread")
            t = threading.Thread(target=self.execute_thread, args=(users, function_to_execute))
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
