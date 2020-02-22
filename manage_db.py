import json
import logging as log
import re
from json import JSONDecodeError
from os import listdir
from os.path import isfile, join

import mysql.connector as mariadb

CONFIG_FILE = ".config.ini"


class ManageDb:
    def __init__(self, local=True):
        self.local = local
        self._maria_usr, self._maria_pwd, self._maria_host, self._maria_db, self._maria_table = self._init_creds()
        self._regexCred = re.compile(
            "[a-zA-Z0-9\\._-]+@[a-zA-Z0-9\\.-]+\.[a-zA-Z]{2,6}[\\rn :\_\-]{1,10}[a-zA-Z0-9\_\-]+")
        self._privileges = {}
        self.__init_db()
        self._connection, self._cursor = self.__connection()
        if not local and ("CREATE" or "ALL PRIVILEGES") in self._privileges[self._maria_db + ".*"]:
            self.__create_table()

    def close_connection(self):
        self._cursor.close()
        self._connection.close()

    def _init_creds(self):
        try:
            with open(CONFIG_FILE, "r") as f:
                json_data = f.read()
                data = json.loads(json_data)
        except JSONDecodeError and FileNotFoundError:
            data = {"local": {}, "remote": {}}
            local_usr = input("Local usr")
            local_pwd = input("Local pwd")
            local_db = input("Local db")
            local_table = input("Local table")
            data["local"]["usr"] = local_usr
            data["local"]["pwd"] = local_pwd
            data["local"]["host"] = "localhost"
            data["local"]["db"] = local_db
            data["local"]["table"] = local_table

            remote_usr = input("Remote usr")
            remote_pwd = input("Remote pwd")
            remote_host = input("Remote host")
            remote_db = input("Remote db")
            remote_table = input("Remote table")
            data["remote"]["usr"] = remote_usr
            data["remote"]["pwd"] = remote_pwd
            data["remote"]["host"] = remote_host
            data["remote"]["db"] = remote_db
            data["remote"]["table"] = remote_table
            with open(CONFIG_FILE, "wb") as f:
                f.write(json.dumps(data))
        if self.local:
            json_parsed = data["local"]
        else:
            json_parsed = data["remote"]
        return json_parsed["usr"], json_parsed["pwd"], json_parsed["host"], json_parsed["db"], json_parsed["table"]

    def __connection(self):
        mariadb_connection = mariadb.connect(host=self._maria_host, user=self._maria_usr, password=self._maria_pwd,
                                             database=self._maria_db)
        cursor = mariadb_connection.cursor()
        return mariadb_connection, cursor

    def __init_db(self):
        mariadb_connection = mariadb.connect(host=self._maria_host, user=self._maria_usr, password=self._maria_pwd)
        cursor = mariadb_connection.cursor()
        if not self.local:
            privileges = "show grants for {}".format(self._maria_usr)
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


