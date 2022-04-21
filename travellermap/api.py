import json
import os
import random
from random import Random
from typing import List, Dict
import requests


class TravellerMap:
    BASE_URI: str = 'https://travellermap.com/api/'

    data: Dict[str, List[str]]  # TODO Replace with Dict[str, List[World]]
    _path: str

    def __init__(self, path: str):
        self._path = path
        if os.path.isfile(path):
            with open(path) as f:
                print('Loading data')
                self.data = json.load(f)
        else:
            print('Getting data')
            self._get_sectors()

    def _get_sectors(self) -> None:
        self.data = {}

        res = requests.get(self.BASE_URI + 'universe').json()
        for sector in res["Sectors"]:
            self.data[sector["Names"][0]["Text"]] = []

    def random_sector(self) -> str:
        """Returns a random sector that has at least 50 worlds"""
        while True:
            sector = random.choice(list(self.data))

            self._get_worlds(sector)
            if len(self.data[sector]) >= 50:
                break

            del self.data[sector]

        return sector

    def _get_worlds(self, sector: str) -> None:
        if len(self.data[sector]) > 0:
            return

        res = requests.get(self.BASE_URI + f'search?q=in:"{sector}"').json()
        for item in res["Results"]["Items"]:
            self.data[sector].append(item["World"]["Name"])

    @property
    def sectors(self) -> List[str]:
        return list(self.data.keys())

    def worlds(self, sector: str) -> List[str]:
        if len(self.data[sector]) == 0:
            self._get_worlds(sector)

        return self.data[sector]

    def random_world(self, sector: str) -> str:
        if len(self.data[sector]) == 0:
            self._get_worlds(sector)

        index = Random().randint(0, len(self.data[sector]) - 1)
        return self.data[sector][index]

    def write_data(self):
        with open(self._path, 'w') as f:
            json.dump(self.data, f)
