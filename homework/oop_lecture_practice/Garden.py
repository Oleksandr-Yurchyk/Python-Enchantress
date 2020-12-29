from abc import ABC, abstractmethod

VEGETABLES = ['red_tomato']
FRUITS = ['golden']


class GardenMetaClass(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Garden(metaclass=GardenMetaClass):
    def __init__(self, vegetables, fruits):
        self.vegetables = vegetables
        self.fruits = fruits

    def show_the_garden(self):
        print('I have such vegetables:')
        [print(vegetable.plant_type) for vegetable in self.vegetables]
        print('I have such fruits:')
        [print(fruit.plant_type) for fruit in self.fruits]


class Vegetables(ABC):
    def __init__(self, vegetable_type):
        self.plant_type = vegetable_type

    states = {0: 'None', 1: 'Flowering', 2: 'Green', 3: 'Red'}

    @property
    def plant_type(self):
        return self._plant_type

    @plant_type.setter
    def plant_type(self, plant_type):
        if plant_type.lower() in VEGETABLES:
            self._plant_type = plant_type
        else:
            raise Exception(f'There is no such vegetables in the list. Your vegetable: {plant_type}')

    @abstractmethod
    def grow(self):
        raise NotImplemented('You missed me.')

    @abstractmethod
    def is_ripe(self):
        raise NotImplemented('You missed me.')


class Fruits(ABC):
    def __init__(self, fruit_type):
        self.plant_type = fruit_type

    states = {0: 'None', 1: 'Flowering', 2: 'Almost_ripe', 3: 'Ripe'}

    @abstractmethod
    def grow(self):
        raise NotImplemented('You missed me.')

    @abstractmethod
    def is_ripe(self):
        raise NotImplemented('You missed me.')

    @property
    def plant_type(self):
        return self._plant_type

    @plant_type.setter
    def plant_type(self, plant_type):
        if plant_type.lower() in FRUITS:
            self._plant_type = plant_type
        else:
            raise Exception(f'There is no such fruits in the list. Your fruits: {plant_type}')


class Tomato(Vegetables):
    def __init__(self, index, vegetable_type):
        super().__init__(vegetable_type)
        self.index = index
        self.state = 0
        self.vegetable_type = vegetable_type

    def grow(self):
        self._change_state()

    def is_ripe(self):
        if self.state == 3:
            return True
        return False

    def _change_state(self):
        if self.state < 3:
            self.state += 1
        self.print_state()

    def print_state(self):
        print(f'{self.vegetable_type} {self.index} is {Tomato.states[self.state]}')


class Apple(Fruits):
    def __init__(self, index, fruit_type):
        super().__init__(fruit_type)
        self.index = index
        self.state = 0
        self.fruit_type = fruit_type

    def grow(self):
        self._change_state()

    def is_ripe(self):
        if self.state == 3:
            return True
        return False

    def _change_state(self):
        if self.state < 3:
            self.state += 1
        self.print_state()

    def print_state(self):
        print(f'{self.fruit_type} {self.index} is {Apple.states[self.state]}')


class TomatoBush:
    def __init__(self, num):
        self.tomatoes = [Tomato(index, 'Red_tomato') for index in range(0, num - 1)]

    def grow_all(self):
        for tomato in self.tomatoes:
            tomato.grow()

    def are_all_ripe(self):
        return all([tomato.is_ripe() for tomato in self.tomatoes])

    def give_away_all(self):
        self.tomatoes = []


class AppleTree:
    def __init__(self, num):
        self.apples = [Apple(index, 'Golden') for index in range(0, num)]

    def grow_all(self):
        for apple in self.apples:
            apple.grow()

    def are_all_ripe(self):
        return all([apple.is_ripe() for apple in self.apples])

    def give_away_all(self):
        self.apples = []


class Gardener:
    def __init__(self, name, plants):
        self.name = name
        self.plants = plants

    def harvest(self):
        print(f'Gardener {self.name} is harvesting...')
        for plant in self.plants:
            if plant.are_all_ripe():
                plant.give_away_all()
                print(f'Harvesting of {plant.__class__.__name__} is finished')
            else:
                print('Too early! Your plant is not ripe.')

    def handling(self):
        print('Gardener is working...')
        for plant in self.plants:
            plant.grow_all()
        print('Gardener finished his work')

    def check_states(self):
        for plant in self.plants:
            if plant.state == 3:
                return True
            return False


if __name__ == '__main__':
    tomato_bush = TomatoBush(4)
    apple_tree = AppleTree(3)

    garden = Garden(vegetables=tomato_bush.tomatoes, fruits=apple_tree.apples)
    garden.show_the_garden()

    gardener = Gardener('Alex', [tomato_bush, apple_tree])
    for i in range(3):
        gardener.handling()

    gardener.harvest()
    if not [print(tomato.plant_type) for tomato in tomato_bush.tomatoes]:
        print(f'Gardener {gardener.name} harvested all of {tomato_bush.__class__.__name__}')

    if not [print(apple.plant_type) for apple in apple_tree.apples]:
        print(f'Gardener {gardener.name} harvested all of {apple_tree.__class__.__name__}')
