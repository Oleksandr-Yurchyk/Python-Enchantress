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
        for i in range(len(self.houses)):
            print(f'House #{i}: area - {self.houses[i].area} m2, cost - {self.houses[i].cost}$\n')

    # Give a discount 5% by realtor
    def client_discount(self):
        if self.discount:
            percent_of_discount = 5  # Percentage can be 0..100
            for house in self.houses:
                amount_of_discount = int(house.cost * (percent_of_discount / 100))
                print(f'{self.name} give {percent_of_discount}% or {amount_of_discount}$ discount to '
                      f'{self.client.name}')
                house.cost -= amount_of_discount
        else:
            print(f'Sorry {self.name} can`t give you a discount')

    # Steal all your money with 10% chance
    def steal_client_money(self):
        if random.randint(1, 100) <= 10:
            self.client.budget = 0
            print(f'{self.name} stole all money from client {self.client.name}')
