import random


class Item(object):
    def __init__(self):
        super(Item, self).__init__()
        self.weight1 = None
        self.weight2 = None
        self.weight3 = None
        self.weight4 = None
        self.weight5 = None
        self.weight6 = None
        self.weight7 = None
        self.weight8 = None
        self.weight9 = None
        self.weight10 = None

    @classmethod
    def random(cls):
        item = Item()
        item.weight1 = random.randint(0, 10)
        item.weight2 = random.randint(0, 10)
        item.weight3 = random.randint(0, 10)
        item.weight4 = random.randint(0, 100)
        item.weight5 = random.randint(0, 100)
        item.weight6 = random.randint(0, 100)
        item.weight7 = random.randint(0, 1000)
        item.weight8 = random.randint(0, 1000)
        item.weight9 = random.randint(0, 1000)
        item.weight10 = random.random()
        return item
