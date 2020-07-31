import logging as log
import random

import numpy
import requests

from catchEmAll.proxyrequests.proxy import Proxy


class NordVpn(Proxy):

    def __init__(self, max_load=50):
        self._nord_api_url = "https://api.nordvpn.com/v1"
        super().__init__("nordvpn")
        self._max_load = max_load
        self._countries = self._get_countries_id()
        server_name = random.choice(list(self._countries.keys()))
        self._servers: {} = {server_name: self._get_working_server(server_name)}
        log.debug("NordProxy Ready")

    def remove_proxy(self):
        self._servers[self._nation].remove(self._current_server)

    def _get_random_server(self, usr: str, pwd: str, nation: str = None):
        if nation and nation in self._countries.keys():
            self._nation = nation
        else:
            self._nation = random.choice(list(self._countries.keys()))
        try:
            self._servers[self._nation]
        except KeyError:
            self._servers[self._nation] = self._get_working_server(self._nation)
        log.debug("Nordvpn: changing server")
        values = numpy.concatenate(list(self._servers.values()), axis=0)
        self._current_server = random.choice(values)
        return "https://{}:{}@{}:80".format(usr, pwd, self._current_server)

    def _get_countries_id(self) -> {str: str}:
        url = self._nord_api_url + "/servers/countries"

        servers = requests.get(url)
        countries = {}
        for srv in servers.json():
            countries[srv["name"]] = srv["id"]

        log.debug("Nordvpn: countries initialized")
        return countries

    def _get_working_server(self, country_name) -> list:
        country_id = self._countries[country_name]
        list_servers = []
        # trial and error, undocumented API
        url = self._nord_api_url + "/servers/recommendations"
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
            filtered = [srv for srv in servers.json() if srv["load"] <= self._max_load]
            for srv in filtered:
                list_servers.append(srv["station"])

        log.debug("Nordvpn: servers for {} initialized".format(country_name))
        return list_servers
