import mysql.connector as mariadb
import logging as log
from os.path import isfile, join
from os import listdir
import re


class ManageDb:
    def __init__(self):
        with open(".config.ini", "r") as f:
            self.maria_usr, self.maria_pwd = f.readline().split(":")
        self.maria_db = "Leaks"
        self.maria_table = "Leaks"
        self.regexCred = re.compile(
            "[a-zA-Z0-9\\._-]+@[a-zA-Z0-9\\.-]+\.[a-zA-Z]{2,6}[\\rn :\_\-]{1,10}[a-zA-Z0-9\_\-]+")
        self.__init_db()
        self.connection, self.cursor = self.__create_table()

    def __init_db(self):
        mariadb_connection = mariadb.connect(host="localhost", user=self.maria_usr, password=self.maria_pwd)
        cursor = mariadb_connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS `{}`".format(self.maria_db))
        log.info("Database created")
        mariadb_connection.disconnect()

    def __create_table(self):
        mariadb_connection = mariadb.connect(host="localhost", user=self.maria_usr, password=self.maria_pwd,
                                             database=self.maria_db)
        cursor = mariadb_connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS `{}` (
                       `email` VARCHAR(320) NOT NULL,
                       `password` VARCHAR(320) NOT NULL,
                       PRIMARY KEY (email,password)
                       )""".format(self.maria_table))
        log.info("Table Leaks created")
        mariadb_connection.commit()
        return mariadb_connection, cursor

    def populate_db(self, mypath):

        for name_file in listdir(mypath):
            file_path = join(mypath, name_file)
            if isfile(file_path):
                with open(file_path, "r") as f:
                    text = f.read()
                    itr = self.regexCred.finditer(text)
                    for elem in itr:
                        elem = elem.group()
                        creds = (elem.split(":")[0], elem.split(":")[1])
                        log.info("Inserting {}".format(creds))
                        insert = "INSERT IGNORE INTO Leaks(email,password) VALUES (%s,%s) "
                        self.cursor.execute(insert, creds)

    def add_column(self, name):
        self.cursor.execute("ALTER TABLE Leaks ADD COLUMN IF NOT EXISTS {} BOOLEAN".format(name))
        self.connection.commit()

    def update_result(self, usr, pwd, column, result):
        update = "UPDATE Leaks SET {} = {} WHERE email= '{}' AND password= '{}'".format(column, result, usr, pwd)
        self.cursor.execute(update)
        self.connection.commit()

    def retrieve_users(self, column, value):
        select = "SELECT email,password from Leaks where {} is {}".format(column, value)
        self.cursor.execute(select)
        users = self.cursor.fetchall()
        return users

    def retrieve_proxies_names(self):
        """
        It retrieve every column that has `Proxy` in his name, so please be coherent or change this shit
        """
        select = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{}'".format(self.maria_table)
        self.cursor.execute(select)
        lists = self.cursor.fetchall()
        results = []
        for table in lists:
            for column in table:
                if "Proxy" in str(column):
                    results.append(column)

        return results
