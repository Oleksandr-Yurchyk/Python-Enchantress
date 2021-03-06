import random


class SingletonMetaClass(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Realtor(metaclass=SingletonMetaClass):
    def __init__(self, name: str, houses: list, client, discount: bool = False):
        self.name = name
        self.houses = houses
        self.client = client
        self.discount = discount

    # Provide information about all the Houses
    def info_about_houses(self):
        for house in self.houses:
            print(f'{house.title}: area - {house.area} m2, cost - {house.cost}$')
        print()

    # Give a discount 5% by realtor
    def client_discount(self):
        if self.discount:
            percent_of_discount = 5  # Percentage can be 0..100
            return percent_of_discount
        print(f'Sorry {self.name} can`t give you a discount')

    # Steal all your money with 10% chance
    def steal_client_money(self):
        print(f'Realtor trying to steal money in {self.client.name}')
        if random.randint(1, 100) <= 10:
            self.client.budget = 0
            print(f'{self.name} stole all money from client {self.client.name}')
        else:
            print(f'Realtor {self.name} could not steal money from client {self.client.name}')
