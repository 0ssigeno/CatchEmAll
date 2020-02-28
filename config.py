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


def write_main(local: bool, max_threads: int, max_threading_functions: int, max_req_same_proxy: int,
               pokedex: str, path_population: str):
    config["MAIN"] = {"local": local, "max_threads": max_threads, "max_threading_functions": max_threading_functions,
                      "max_req_same_proxy": max_req_same_proxy, "pokedex": pokedex,
                      "path_population": path_population}
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)


def read_main():
    config.read(CONFIG_FILE)
    main = config["MAIN"]
    return main["local"], main["max_threads"], main["max_threading_functions"], main["max_req_same_proxy"], \
           main["pokedex"], main["path_population"]
