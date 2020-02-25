import configparser

CONFIG_FILE = ".config.ini"

config = configparser.ConfigParser()


def write_tor(passphrase: str):
    config["TOR"] = {"passphrase": passphrase}
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)


def read_tor():
    config.read(CONFIG_FILE)
    return config["TOR"]["passphrase"]


def write_mariadb(local: bool, usr: str, pwd: str, host: str, db: str, table: str):
    if local:
        name = "MARIA_LOCAL"
    else:
        name = "MARIA_REMOTE"
    config[name] = {"usr": usr, "pwd": pwd, "host": host, "db": db, "table": table}
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)


def read_mariadb(local: bool):
    if local:
        name = "MARIA_LOCAL"
    else:
        name = "MARIA_REMOTE"
    config.read(CONFIG_FILE)
    part_config = config[name]
    return part_config["usr"], part_config["pwd"], part_config["host"], part_config["db"], part_config["table"]
