import random
from abc import ABC, abstractmethod
from Realtor import Realtor

PRICE_PER_SQUARE_METER = 500


class House:
    def __init__(self):
        self.area = random.randrange(20, 80, 10)
        self.cost = self.area * PRICE_PER_SQUARE_METER
        if self.area < 30:
            self.title = 'Cottage'
        elif 30 <= self.area < 60:
            self.title = 'Villa'
        else:
            self.title = 'Penthouse'


class Human(ABC):

    @abstractmethod
    def info_about_myself(self):
        raise NotImplemented('It seems you forgot about me')

    @abstractmethod
    def make_money(self):
        raise NotImplemented('It seems you forgot about me')

    @abstractmethod
    def buy_house(self, house_cost: int):
        raise NotImplemented('It seems you forgot about me')


class Person(Human):
    def __init__(self, name: str, age: int, availability_of_money: bool, have_home: bool):
        self.name = name
        self.age = age
        self.budget = 0
        if availability_of_money:
            self.budget = 5000
        self.salary = 1000
        self.have_home = have_home

    def buy_house(self, houses: list):
        for house in houses:
            if self.budget > house.cost:
                self.budget -= house.cost
                self.have_home = True
                houses.remove(house)
                print(f'Congrats! {self.name} have bought a house for {house.cost}$. His budget after purchase is - '
                      f'{self.budget}$\n')
            else:
                print(f'{self.name} haven`t enough money to buy {house.title}')

    def make_money(self):
        self.budget += self.salary

    def info_about_myself(self):
        print(f'{self.name}, {self.age} y.o, have budget - {self.budget}$, have own home - {self.have_home}')

    def work_1_year(self):
        for _ in range(12):
            self.make_money()
        self.age += 1
        print(f'{self.name} have worked 1 year with salary {self.salary}$ and earn {self.salary * 12}$')

    def apply_discount(self, houses: list, percent_of_discount):
        for house in houses:
            amount_of_discount = int(house.cost * (percent_of_discount / 100))
            print(f'{self.name} got {percent_of_discount}% or {amount_of_discount}$ discount to the {house.title}')
            house.cost -= amount_of_discount
        print()


if __name__ == '__main__':
    alex = Person('Alex', 20, availability_of_money=False, have_home=False)
    available_houses = [House() for _ in range(5)]
    realtor = Realtor('John', available_houses, client=alex, discount=True)

    # Houses info before discount
    realtor.info_about_houses()

    # Applying discount
    realtor_disc = realtor.client_discount()
    alex.apply_discount(available_houses, realtor_disc)

    # Houses info after discount
    realtor.info_about_houses()

    alex.info_about_myself()

    while not alex.have_home:
        alex.work_1_year()
        alex.buy_house(available_houses)

    alex.info_about_myself()

    # Realtor try to steal money
    realtor.steal_client_money()

    alex.info_about_myself()
