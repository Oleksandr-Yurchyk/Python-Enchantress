import unittest
from unittest.mock import patch
from unittest import mock
from hen_house.hen_class import HenHouse, ErrorTimesOfYear


class TestHenHouse(unittest.TestCase):

    def setUp(self) -> None:
        self.house = HenHouse(20)

    def test_wrong_hen_count(self):
        self.assertRaises(ValueError, lambda: self.house.__init__(4))

    def test_correct_hen_count(self):
        self.assertEqual(self.house.__init__(6), None)

    def test_season_winter(self):
        with patch('hen_house.hen_class.datetime.datetime') as _mock:
            _mock.today().month = 1
            self.assertEqual(self.house.season, 'winter')

    def test_season_summer(self):
        with patch('hen_house.hen_class.datetime.datetime') as _mock:
            _mock.today().month = 6
            self.assertEqual(self.house.season, 'summer')

    @patch('hen_house.hen_class.HenHouse.season', 'summer')
    def test_productivity_index(self):
        self.assertEqual(self.house._productivity_index(), self.house.hens_productivity.get('summer'))

    @patch('hen_house.hen_class.HenHouse.season', 'incorrect_season')
    def test_productivity_index_incorrect_season(self):
        self.assertRaises(ErrorTimesOfYear, lambda: self.house._productivity_index())

    @patch('hen_house.hen_class.HenHouse._productivity_index', mock.Mock(return_value=0.25))
    def test_get_eggs_daily_in_winter(self):
        self.assertEqual(self.house.get_eggs_daily(5), 1)

    @patch('hen_house.hen_class.HenHouse._productivity_index', mock.Mock(return_value=1))
    def test_get_eggs_daily_in_summer(self):
        self.assertEqual(self.house.get_eggs_daily(5), 5)

    @patch('hen_house.hen_class.HenHouse.season', 'winter')
    def test_get_max_count_for_soup(self):
        self.assertEqual(self.house.get_max_count_for_soup(3), 8)

    @patch('hen_house.hen_class.HenHouse.season', 'winter')
    def test_get_max_count_for_soup_returns_zero(self):
        self.assertEqual(self.house.get_max_count_for_soup(5), 0)

    def test_food_price(self):
        with patch('hen_house.hen_class.requests.get') as response:
            response.return_value.status_code = 200
            self.assertIsInstance(self.house.food_price(), int)

    def test_food_price_connection_error(self):
        with patch('hen_house.hen_class.requests.get') as response:
            response.return_value.status_code = 404
            self.assertRaises(ConnectionError, lambda: self.house.food_price())


if __name__ == '__main__':
    unittest.main()
