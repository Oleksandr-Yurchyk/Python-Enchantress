class Animal:

    @staticmethod
    def move():
        print('I can move')


class Mammal(Animal):

    @staticmethod
    def about_mammal():
        print('I have the properties of a Mammal')


class Predator(Mammal):

    @staticmethod
    def about_predator():
        print('I have the properties of a Predator')


class Pet(Predator):

    @staticmethod
    def about_pet():
        print('I`m a pet, and also i`m human`s best friend')


class Dog(Pet):

    @staticmethod
    def protect_house():
        print('I should protect the house! Woof-woof')


if __name__ == '__main__':
    rex = Dog()
    rex.move()
    rex.about_mammal()
    rex.about_predator()
    rex.about_pet()
    rex.protect_house()
