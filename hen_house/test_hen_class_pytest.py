import pytest
from hen_house.hen_class import HenHouse, ErrorTimesOfYear


@pytest.fixture(scope='function')
def house():
    house = HenHouse(20)
    yield house


class TestHenClassPositive:

    @pytest.mark.parametrize(
        'hen_count',
        (
                5, 7, 9
        )
    )
    def test_hen_count_positive(self, house, hen_count):
        assert house.__init__(hen_count) is None

    @pytest.mark.parametrize(
        "month, season",
        (
                (1, 'winter'),
                (3, 'spring'),
                (6, 'summer'),
                (9, 'autumn'),
        )
    )
    def test_season_positive(self, mocker, house, month, season):
        mock = mocker.patch('hen_house.hen_class.datetime.datetime')
        mock.today().month = month
        assert house.season == season

    @pytest.mark.parametrize(
        "month",
        (1, 3, 6, 9)
    )
    def test_season_is_instance_of_str(self, mocker, house, month):
        mock = mocker.patch('hen_house.hen_class.datetime.datetime')
        mock.today().month = month
        assert isinstance(house.season, str)

    @pytest.mark.parametrize(
        'season',
        (
                'winter',
                'spring',
                'summer',
                'autumn'
        )
    )
    def test_productivity_index_positive(self, mocker, house, season):
        mock = mocker.patch('hen_house.hen_class.HenHouse.season', new_callable=mocker.PropertyMock)
        mock.return_value = season
        assert house._productivity_index() == house.hens_productivity.get(season)

    @pytest.mark.parametrize(
        'season, expected_res',
        (
                ('winter', 1),
                ('autumn', 2),
                ('spring', 3),
                ('summer', 5)
        )
    )
    def test_get_eggs_daily_positive(self, mocker, house, season, expected_res):
        mock = mocker.patch('hen_house.hen_class.HenHouse.season', new_callable=mocker.PropertyMock)
        mock.return_value = season
        assert house.get_eggs_daily(5) == expected_res

    @pytest.mark.parametrize(
        'season, expected_res',
        (
                ('winter', 8),
                ('spring', 16),
                ('summer', 17),
                ('autumn', 14),
        )
    )
    def test_get_max_count_for_soup_positive(self, mocker, house, season, expected_res):
        mock = mocker.patch('hen_house.hen_class.HenHouse.season', new_callable=mocker.PropertyMock)
        mock.return_value = season
        assert house.get_max_count_for_soup(3) == expected_res

    def test_food_price_positive(self, mocker, house):
        mock = mocker.patch('hen_house.hen_class.requests.get')
        mock.return_value.status_code = 200
        assert isinstance(house.food_price(), int)


class TestHenClassNegative:

    @pytest.mark.parametrize(
        'hen_count',
        (
                -1, 0, 4
        )
    )
    def test_hen_count_failure(self, house, hen_count):
        pytest.raises(ValueError, lambda: house.__init__(hen_count))

    @pytest.mark.parametrize(
        "month, season",
        (
                (1, 'spring'),
                (3, 'summer'),
                (6, 'autumn'),
                (9, 'winter'),
        )
    )
    def test_season_negative(self, mocker, house, month, season):
        mock = mocker.patch('hen_house.hen_class.datetime.datetime')
        mock.today().month = month
        assert house.season != season

    @pytest.mark.parametrize(
        'season',
        (
                'not a season',
                'month',
        )
    )
    def test_productivity_index_failure(self, mocker, house, season):
        mock = mocker.patch('hen_house.hen_class.HenHouse.season', new_callable=mocker.PropertyMock)
        mock.return_value = season
        pytest.raises(ErrorTimesOfYear, lambda: house._productivity_index())

    def test_food_price_failure(self, mocker, house):
        mock = mocker.patch('hen_house.hen_class.requests.get')
        mock.return_value.status_code = 404
        pytest.raises(ConnectionError, lambda: house.food_price())
