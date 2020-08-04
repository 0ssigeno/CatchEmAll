import logging as log
import re
from multiprocessing import Lock
from os import listdir
from os.path import isfile, join

import mysql.connector as mariadb
from mysql.connector.errors import ProgrammingError


# TODO fare decoratore con mutex per le funzioni

class DbManager:
    def __init__(self, usr: str, pwd: str, host: str, db: str):
        self.mutex = Lock()
        self.local = True if host == "localhost" else False
        self.usr = usr
        self.pwd = pwd
        self.host = host
        self.table = "Accounts"
        self.db = db
        self._regexCred = re.compile(
            "[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}[\\rn :_\-]{1,10}[a-zA-Z0-9_\-]+")
        self._privileges = {}
        # self._connection, self._cursor = self.__connection()
        # if local or ("CREATE" or "ALL PRIVILEGES") in self._privileges[self._maria_db + ".*"]:
        #     self.__create_table()

    def initialize(self):
        if self.local:
            self._connection = mariadb_connection = mariadb.connect(host=self.host, user=self.usr, password=self.pwd)
            self._cursor = mariadb_connection.cursor(buffered=True)

            self._cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(self.db))
            self._connection.commit()
            log.debug("database checked")
            self._cursor.execute("USE {}".format(self.db))
            self._cursor.execute("""CREATE TABLE IF NOT EXISTS `{}` (
                                    `id` int(11) NOT NULL AUTO_INCREMENT,
                                   `email` VARCHAR(320) NOT NULL,
                                   `password` VARCHAR(320) NOT NULL,
                                   PRIMARY KEY (id)
                                   )""".format(self.table))
            self._connection.commit()
            log.debug("Base table checked")
        else:
            raise NotImplementedError("Not local db is not implemented")

    def login(self):
        self._connection = mariadb.connect(host=self.host, user=self.usr, password=self.pwd, database=self.db)
        self._cursor = self._connection.cursor(buffered=True)

    def close_connection(self):
        self._cursor.close()
        self._connection.close()

    def populate_db(self, ail_directory_path: str):

        for name_file in listdir(ail_directory_path):
            file_path = join(ail_directory_path, name_file)
            if isfile(file_path):
                with open(file_path, "r") as f:
                    text = f.read()
                    itr = self._regexCred.finditer(text)
                    credentials = []
                    for elem in itr:
                        elem = elem.group()
                        creds = (elem.split(":")[0], elem.split(":")[1])
                        credentials.append(creds)
                    self.add_users(credentials)
            else:
                # TODO recursive
                pass

    def add_users(self, credentials: [tuple]):
        self.mutex.acquire()
        insert = "INSERT IGNORE INTO {}(email,password) VALUES (%s,%s) ".format(self.table)
        for creds in credentials:
            self._cursor.execute(insert, creds)
        self._connection.commit()
        self.mutex.release()

    def add_table(self, table):
        self.mutex.acquire()
        self._cursor.execute("""CREATE TABLE IF NOT EXISTS `{}` (
                                            `id` int(11) NOT NULL REFERENCES Accounts(id),
                                           PRIMARY KEY (id)
                                           )""".format(table))
        self._connection.commit()
        self.mutex.release()

    def add_column(self, column: str):
        self.mutex.acquire()
        self._cursor.execute("ALTER TABLE {} ADD COLUMN IF NOT EXISTS {} BOOLEAN".format(self.table, column))
        self._connection.commit()
        self.mutex.release()

    def update_result(self, usr: str, pwd: str, result: bool, column: str):
        self.mutex.acquire()

        update = "UPDATE {} SET {} = %s WHERE email= %s AND password= %s".format(self.table, column)
        self._cursor.execute(update, (result, usr, pwd))
        self._connection.commit()
        self.mutex.release()

    def retrieve_value_user(self, email: str, pwd: str, column: str) -> str:
        self.mutex.acquire()

        select = "SELECT {} from {} where email = %s and password = %s".format(column, self.table)
        self._cursor.execute(select, (email, pwd))
        value_user = self._cursor.fetchone()[0]
        self.mutex.release()

        return value_user

    def retrieve_values_user(self, email: str, pwd: str, columns: list) -> list:
        self.mutex.acquire()

        columns = ", ".join(columns)
        select = "SELECT {} from {} where email = %s and password = %s".format(columns, self.table)
        self._cursor.execute(select, (email, pwd))
        values_user = list(self._cursor.fetchone())
        self.mutex.release()

        return values_user

    def retrieve_users(self, column: str, value: bool or None):
        self.mutex.acquire()
        if value is None:
            comparator = "is"
        else:
            comparator = "="
        try:
            select = "SELECT email,password from {} where {} {} %s".format(self.table, column, comparator)
            self._cursor.execute(select, (value,))
            users = self._cursor.fetchall()
        except ProgrammingError as e:
            log.warning("You don't have a {} column".format(column))
            users = []
        self.mutex.release()
        return users

    def retrieve_all(self):
        self.mutex.acquire()

        select = "SELECT email, password from {} ".format(self.table)
        self._cursor.execute(select)
        users = self._cursor.fetchall()
        self.mutex.release()

        return users

    def delete_db(self, db):
        self.mutex.acquire()
        delete = "drop database {}".format(db)
        self._cursor.execute(delete)
        self.mutex.release()
