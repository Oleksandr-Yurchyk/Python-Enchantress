Meta = type('Meta', (), {'name': 'Michael'})
SubMeta = type('Meta', (Meta,), {})


class Human(SubMeta):
    def say_hi(self):
        print(f'Hi! My name is {self.name}')


if __name__ == '__main__':
    user = Human()
    user.say_hi()
