class Processor:
    def __init__(self):
        self.developer = 'Apple Inc.'
        self.model = 'M1'


class Laptop:
    def __init__(self, brand: str, model:str):
        self.brand = brand
        self.model = model
        self.inch = "15'6"
        self.processor = Processor()


if __name__ == '__main__':
    macbook = Laptop('Apple', 'Macbook Pro')
    print(macbook.brand)
    print(macbook.model)
    print(macbook.inch)
    print(macbook.processor.developer)
    print(macbook.processor.model)
