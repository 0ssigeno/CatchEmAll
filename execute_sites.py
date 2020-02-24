import logging as log
import concurrent.futures
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

    def __init__(self, max_req_same_proxy=5, max_threads_users=2, max_threading_functions=1, local=True):
        self._max_req_same_proxy = max_req_same_proxy
        self._max_threading_users = max_threads_users
        self._max_threading_functions = max_threading_functions
        self._local = local

    @staticmethod
    def __save_results(mr: ManageRequests, results: dict, usr: str, pwd: str):
        for key in results.keys():
            if not results[key]:
                log.info("Account error {}:{} on site {} ".format(usr, pwd, key))
            else:
                log.info("Account valid {}:{} on site {} ".format(usr, pwd, key))
            mr.db.update_result(usr, pwd, key, results[key])

    def __execute_thread(self, users: list, functions_to_execute: list, sites: list):
        """
        function_to_execute is the function that the user define for scrape a single site
        """
        mr = ManageRequests(local=self._local)
        mr.set_random_proxy()
        mr.set_random_user_agent()

        counter_executions_for_user = 0
        for creds in users:
            usr = creds[0]
            pwd = creds[1]
            with concurrent.futures.ThreadPoolExecutor(max_workers=self._max_threading_functions) as executor:
                # todo optimize via sql
                [mr.db.add_column(site) for site in sites]
                # todo optimize via sql
                values = [mr.db.retrieve_value_user(usr, pwd, site) for site in sites]

                future_exs = {executor.submit(function_to_execute, usr, pwd, mr)
                              : function_to_execute.__name__ for value, function_to_execute in
                              zip(values, functions_to_execute)
                              if value is None}
                # I want to change proxy only on real requests, not every single user
                if None in values:
                    counter_executions_for_user += 1
                # Dict of function:result for every user
                res = {}
                for future in concurrent.futures.as_completed(future_exs):
                    res[future_exs[future]] = future.result()

                # Decided to save after every user just because i will probably stop the program before trying every
                # user
                if res:
                    self.__save_results(mr, res, usr, pwd)

            if counter_executions_for_user == self._max_req_same_proxy:
                counter_executions_for_user = 0
                mr.set_random_proxy()
                mr.set_random_user_agent()

    def test_sites(self, functions_to_execute: list, columns: list):
        """
            Create a column for the site that wants to be tested, if is not already present
            Retrieve every users that must be tested
            Divide users in equal parts, each subset will have its own thread
        """
        db = ManageDb(local=self._local)
        users = db.retrieve_all()
        db.close_connection()
        log.info("We are going to test {} users".format(len(users)))
        list_users = chunks(users, self._max_threading_users)
        log.info("Every thread has {} user".format(len(list_users[0])))
        with concurrent.futures.ThreadPoolExecutor(max_workers=self._max_threading_users) as executor:
            [executor.submit(self.__execute_thread, users, functions_to_execute, columns) for users in list_users]

    def populate_db(self, path):
        db = ManageDb(local=self._local)
        db.populate_db(path)
        db.close_connection()
