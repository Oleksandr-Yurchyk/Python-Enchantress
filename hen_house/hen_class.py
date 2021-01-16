import datetime
import requests


class ErrorTimesOfYear(Exception):
    pass


class HenHouse:
    min_hens_accepted = 5
    hens_productivity = {'winter': 0.25, 'spring': 0.75, 'autumn': 0.5, 'summer': 1}

    def __init__(self, hen_count: int):
        self.hen_count = hen_count
        if self.hen_count < self.min_hens_accepted:
            raise ValueError('You need more hens))')
        else:
            print("You have enough hens!!!")

    @property
    def season(self) -> str:
        today = datetime.datetime.today()
        if today.month in [12, 1, 2]:
            return "winter"
        elif today.month in [0, 3, 4, 5]:
            return "spring"
        elif today.month in [6, 7, 8]:
            return "summer"
        elif today.month in [9, 10, 11]:
            return "autumn"

    def _productivity_index(self):
        if self.season in self.hens_productivity:
            return self.hens_productivity[self.season]
        raise ErrorTimesOfYear

    def get_eggs_daily(self, hen_count) -> int:
        return int(hen_count * self._productivity_index())

    def get_max_count_for_soup(self, expected_for_tomorrow_eggs) -> int:
        if self.hen_count < self.min_hens_accepted or self.get_eggs_daily(self.hen_count) < expected_for_tomorrow_eggs:
            return 0
        else:
            return int((self.get_eggs_daily(self.hen_count) - expected_for_tomorrow_eggs) / self._productivity_index())

    @staticmethod
    def food_price() -> int:
        page = requests.get("http:/chicken/food")
        if page.status_code == 200:
            return int(page.text[10])
        else:
            raise ConnectionError()
