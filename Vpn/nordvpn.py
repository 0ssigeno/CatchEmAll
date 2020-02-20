import logging as log
import random

import requests

nord_api_base = "https://api.nordvpn.com/v1"


class NordVpn:
    """
    Describe
    """

    def __init__(self, request_before_change_server=10):

        self.default_max_load = 50
        self.countries = self.__get_countries_id()
        self.position_server = 0
        self.request_before_change_server = request_before_change_server
        self.servers = self.__get_working_server(self.position_server)
        log.info("Nordvpn: countries initialized")
        self.count_request = 0

    def get_random_server(self):
        self.count_request += 1
        if self.request_before_change_server:
            self.count_request = 0
            self.position_server = (self.position_server + 1) % len(self.servers)
            log.info("Nordvpn: changing country")
            self.servers = self.__get_working_server(self.position_server)
        log.info("Nordvpn: changing server")
        return random.choice(self.servers)

    @staticmethod
    def __get_countries_id():
        url = nord_api_base + "/servers/countries"

        servers = requests.get(url)
        countries = {}
        for srv in servers.json():
            countries[srv["name"]] = srv["id"]
        log.info("Nordvpn countries initalized")
        return countries

    def __get_working_server(self, position):
        list_servers = []
        country_name = sorted(self.countries)[position]
        country_id = self.countries[country_name]
        # trial and error, undocumented API
        url = nord_api_base + "/servers/recommendations"
        params = {
            "limit": 16384,
            "filters[country_id]": country_id,
            "fields[servers.name]": "",
            "fields[servers.locations.country.code]": "",
            "fields[servers.locations.country.city.name]": "",
            "fields[station]": "",
            "fields[load]": "",
            "fields[servers.groups.title]": "",
        }

        servers = requests.get(url, params=params)
        if servers:
            filtered = [srv for srv in servers.json() if srv["load"] <= self.default_max_load]
            for srv in filtered:
                list_servers.append(srv["station"])
        return list_servers
