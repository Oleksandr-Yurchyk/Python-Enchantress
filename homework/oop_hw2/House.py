class House:
    def __init__(self, area: int, cost: int):
        self.area = area
        self.cost = cost

    def purchase_discount_10percent(self):
        print(f'Previous owner gives a purchase discount 10% or {int(self.cost * 0.1)}$\n')
        self.cost = int(self.cost * 0.9)
