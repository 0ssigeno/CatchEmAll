import asyncio
import random
from enum import Enum

import proxybroker


class Anonymity(Enum):
    Transparent = "Transparent"
    Anonymous = "Anonymous"
    High = "High"


class ProxyBroker:

    async def insert(self, proxies):
        while True:
            proxy = await proxies.get()
            if proxy is None: break
            self.proxies_found.append(proxy)

    def __init__(self, num_proxies_to_find=20):
        self.proxies_found = []
        self.loop = asyncio.get_event_loop()
        self.num_proxies_to_find = num_proxies_to_find
        self.proxies = asyncio.Queue()
        broker = proxybroker.Broker(self.proxies)
        self.tasks = asyncio.gather(
            broker.find(types=['HTTPS', (Anonymity.Anonymous, Anonymity.High)], limit=num_proxies_to_find),
            self.insert(self.proxies))
        self.loop.run_until_complete(self.tasks)

    def get_random_server(self):
        a = random.choice(self.proxies_found)
        return a
