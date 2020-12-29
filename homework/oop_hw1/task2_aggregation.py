class String:
    def __init__(self):
        self.count = 6
        self.length = 50


class Guitar:
    def __init__(self, string: String):
        self.string = string


if __name__ == '__main__':
    string = String()
    guitar = Guitar(string)
    print(guitar.string.count)
    print(guitar.string.length)
