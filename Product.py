class Product(object):

    def __init__(self, name, unit_price, color):
        self.name = name
        self.unit_price = unit_price
        self.color = color


class Curtain(Product):

    def __init__(self, name, unit_price, color, pile, width,):
        self.pile = pile
        self.width = width
        self.variant_list = []
        super().__init__(name, unit_price, color)

