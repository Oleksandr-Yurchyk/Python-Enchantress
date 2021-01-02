from abc import ABC, abstractmethod
from House import House
from homework.oop_hw2.Realtor import Realtor


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

    def buy_house(self, house: House):
        if self.budget > house.cost:
            self.budget -= house.cost
            self.have_home = True
            print(f'Congrats! {self.name} have bought a house for {house.cost}$. His budget after purchase is - '
                  f'{self.budget}\n')
        else:
            print(f'{self.name} haven`t enough money to buy this house')

    def make_money(self):
        self.budget += self.salary

    def info_about_myself(self):
        print(f'{self.name}, {self.age} y.o, have budget - {self.budget}$, have own home - {self.have_home}')

    def work_1_year(self):
        for _ in range(12):
            self.make_money()
        self.age += 1
        print(f'{self.name} have worked 1 year with salary {self.salary}$ and earn {self.salary * 12}$')


if __name__ == '__main__':
    alex = Person('Alex', 20, availability_of_money=False, have_home=False)
    penthouse = House(area=40, cost=80000)
    realtor = Realtor('John', [penthouse], alex, discount=True)

    # Houses info before discounts
    realtor.info_about_houses()

    # House discounts
    realtor.client_discount()
    penthouse.purchase_discount_10percent()

    # Houses info after discounts
    realtor.info_about_houses()

    alex.info_about_myself()

    while not alex.have_home:
        alex.work_1_year()
        alex.buy_house(penthouse)

    alex.info_about_myself()

    print(f'Realtor trying to steal money in {alex.name}')
    realtor.steal_client_money()

    alex.info_about_myself()
