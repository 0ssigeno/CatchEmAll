import logging as log
import re
from os import listdir
from os.path import isfile, join

import mysql.connector as mariadb


class ManageDb:
    def __init__(self):
        self._config_file = ".config.ini"
        with open(self._config_file, "r") as f:
            self.maria_usr, self.maria_pwd, self.maria_host = f.readline().split(":")
        self._maria_db = "Leaks"
        self._maria_table = "Leaks"
        self._regexCred = re.compile(
            "[a-zA-Z0-9\\._-]+@[a-zA-Z0-9\\.-]+\.[a-zA-Z]{2,6}[\\rn :\_\-]{1,10}[a-zA-Z0-9\_\-]+")
        self._privileges = {}
        self.__init_db()
        self._connection, self._cursor = self.__connection()
        if "CREATE" or "ALL PRIVILEGES" in self._privileges[self._maria_db + ".*"]:
            self.__create_table()

    def __connection(self):
        mariadb_connection = mariadb.connect(host=self.maria_host, user=self.maria_usr, password=self.maria_pwd,
                                             database=self._maria_db)
        cursor = mariadb_connection.cursor()
        return mariadb_connection, cursor

    def __init_db(self):
        mariadb_connection = mariadb.connect(host=self.maria_host, user=self.maria_usr, password=self.maria_pwd)
        cursor = mariadb_connection.cursor()
        privileges = "show grants for {}".format(self.maria_usr)
        cursor.execute(privileges)
        res = cursor.fetchall()

        # TODO FIX THIS SHIT
        for elem in res:
            db = elem[0].split("ON")[1].split("TO")[0].strip().replace("`", "")
            grants = [grant.strip() for grant in elem[0].split(" ON ")[0].split("GRANT")[1].split(",")]
            self._privileges[db] = grants
        if "CREATE" or "ALL PRIVILEGES" in self._privileges["*.*"]:
            cursor.execute("CREATE DATABASE IF NOT EXISTS `{}`".format(self._maria_db))
            log.info("Database checked")
        mariadb_connection.disconnect()

    def __create_table(self):
        self._cursor.execute("""CREATE TABLE IF NOT EXISTS `{}` (
                       `email` VARCHAR(320) NOT NULL,
                       `password` VARCHAR(320) NOT NULL,
                       PRIMARY KEY (email,password)
                       )""".format(self._maria_table))
        log.info("Table {} checked".format(self._maria_table))
        self._connection.commit()

    def populate_db(self, mypath):

        for name_file in listdir(mypath):
            file_path = join(mypath, name_file)
            if isfile(file_path):
                with open(file_path, "r") as f:
                    text = f.read()
                    itr = self._regexCred.finditer(text)
                    for elem in itr:
                        elem = elem.group()
                        creds = (elem.split(":")[0], elem.split(":")[1])
                        log.info("Inserting {}".format(creds))
                        insert = "INSERT IGNORE INTO Leaks(email,password) VALUES (%s,%s) "
                        self._cursor.execute(insert, creds)
        self._connection.commit()

    def add_column(self, name):
        self._cursor.execute("ALTER TABLE Leaks ADD COLUMN IF NOT EXISTS {} BOOLEAN".format(name))
        self._connection.commit()

    def update_result(self, usr, pwd, column, result):
        update = "UPDATE Leaks SET {} = {} WHERE email= '{}' AND password= '{}'".format(column, result, usr, pwd)
        self._cursor.execute(update)
        self._connection.commit()

    def retrieve_value_user(self, email, pwd, column):
        select = "SELECT {} from Leaks where email = '{}' and password = '{}'".format(column, email, pwd)
        self._cursor.execute(select)
        user = self._cursor.fetchone()[0]
        return user

    def retrieve_users(self, column, value):
        select = "SELECT email,password from Leaks where {} is {}".format(column, value)
        self._cursor.execute(select)
        users = self._cursor.fetchall()
        return users

    def retrieve_all(self):
        select = "SELECT email, password from Leaks "
        self._cursor.execute(select)
        users = self._cursor.fetchall()
        return users

    def retrieve_proxies_names(self):
        """
        It retrieve every column that has `Proxy` in his name, so please be coherent or change this shit
        """
        select = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{}'".format(self._maria_table)
        self._cursor.execute(select)
        lists = self._cursor.fetchall()
        results = []
        for table in lists:
            for column in table:
                if "Proxy" in str(column):
                    results.append(column)

        return results
