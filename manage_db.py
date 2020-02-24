import json
import logging as log
import re
from json import JSONDecodeError
from os import listdir
from os.path import isfile, join

import mysql.connector as mariadb

CONFIG_FILE = ".config.ini"


class ManageDb:
    def __init__(self, local: bool = True):
        self.local = local
        self._maria_usr, self._maria_pwd, self._maria_host, self._maria_db, self._maria_table = self._init_credentials()
        self._regexCred = re.compile(
            "[a-zA-Z0-9\\._-]+@[a-zA-Z0-9\\.-]+\.[a-zA-Z]{2,6}[\\rn :\_\-]{1,10}[a-zA-Z0-9\_\-]+")
        self._privileges = {}
        self.__init_db()
        self._connection, self._cursor = self.__connection()
        if local or ("CREATE" or "ALL PRIVILEGES") in self._privileges[self._maria_db + ".*"]:
            self.__create_table()

    def close_connection(self):
        self._cursor.close()
        self._connection.close()

    def _init_credentials(self):
        try:
            with open(CONFIG_FILE, "r") as f:
                json_data = f.read()
                data = json.loads(json_data)
        except JSONDecodeError and FileNotFoundError:
            data = {"local": {}, "remote": {}}
            local_usr = input("Please insert local mariadb usr\n")
            local_pwd = input("Please insert local mariadb pwd\n")
            local_db = input("Please insert local mariadb db\n")
            local_table = input("Please insert local mariadb table\n")
            data["local"]["usr"] = local_usr
            data["local"]["pwd"] = local_pwd
            data["local"]["host"] = "localhost"
            data["local"]["db"] = local_db
            data["local"]["table"] = local_table

            remote_usr = input("Please insert remote mariadb usr\n")
            remote_pwd = input("Please insert remote mariadb pwd\n")
            remote_host = input("Please insert remote mariadb host\n")
            remote_db = input("Please insert remote mariadb db\n")
            remote_table = input("Please insert remote mariadb table\n")
            data["remote"]["usr"] = remote_usr
            data["remote"]["pwd"] = remote_pwd
            data["remote"]["host"] = remote_host
            data["remote"]["db"] = remote_db
            data["remote"]["table"] = remote_table
            with open(CONFIG_FILE, "w") as f:
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
        if self.local or "CREATE" or "ALL PRIVILEGES" in self._privileges["*.*"]:
            cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(self._maria_db))
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

    def populate_db(self, mypath: str):

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
                        insert = "INSERT IGNORE INTO {}(email,password) VALUES (%s,%s) ".format(self._maria_table)
                        self._cursor.execute(insert, creds)
        self._connection.commit()

    def add_column(self, column: str):
        self._cursor.execute("ALTER TABLE {} ADD COLUMN IF NOT EXISTS {} BOOLEAN".format(self._maria_table, column))
        self._connection.commit()

    def update_result(self, usr: str, pwd: str, column: str, result: bool):
        update = "UPDATE {} SET {} = %s WHERE email= %s AND password= %s".format(self._maria_table, column)
        self._cursor.execute(update, (result, usr, pwd))
        self._connection.commit()

    def retrieve_value_user(self, email: str, pwd: str, column: str):
        select = "SELECT {} from {} where email = %s and password = %s".format(column, self._maria_table)
        self._cursor.execute(select, (email, pwd))
        value_user = self._cursor.fetchone()[0]
        return value_user

    def retrieve_values_user(self, email, pwd, columns: list):
        columns = ", ".join(columns)
        select = "SELECT {} from {} where email = %s and password = %s".format(columns, self._maria_table)
        self._cursor.execute(select, (email, pwd))
        values_user = list(self._cursor.fetchone())
        return values_user

    def retrieve_users(self, column: str, value: bool):
        select = "SELECT email,password from {} where {} = %s".format(self._maria_table, column)
        self._cursor.execute(select, (value,))
        users = self._cursor.fetchall()
        return users

    def retrieve_all(self):
        select = "SELECT email, password from {} ".format(self._maria_table)
        self._cursor.execute(select)
        users = self._cursor.fetchall()
        return users
