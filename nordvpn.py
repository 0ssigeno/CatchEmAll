import logging as log
import random

import requests


class NordVpn:
    def __init__(self):
        self.nord_api_base = "https://api.nordvpn.com/v1"
        self.default_max_load = 50
        self.countries = self.__get_countries_id()
        log.info("Nordvpn: countries initialized")

    def __get_countries_id(self):
        url = self.nord_api_base + "/servers/countries"

        servers = requests.get(url)
        countries = {}
        for srv in servers.json():
            countries[srv["name"]] = srv["id"]
        return countries

    def get_working_server(self):
        for country in self.countries:
            country_id = self.countries[country]
            # trial and error, undocumented API
            url = self.nord_api_base + "/servers/recommendations"
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
            filtered = [srv for srv in servers.json() if srv["load"] <= self.default_max_load]

            servers_filtered = [srv["station"] for srv in filtered]
            return random.choice(servers_filtered)
