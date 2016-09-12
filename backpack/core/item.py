import random


class Item(object):
    def __init__(self, weight1=None, weight2=None, weight3=None, weight4=None, weight5=None, weight6=None,
                 weight7=None, weight8=None, weight9=None, weight10=None, value=0):
        super(Item, self).__init__()
        self.weight1 = weight1
        self.weight2 = weight2
        self.weight3 = weight3
        self.weight4 = weight4
        self.weight5 = weight5
        self.weight6 = weight6
        self.weight7 = weight7
        self.weight8 = weight8
        self.weight9 = weight9
        self.weight10 = weight10
        self.value = value

    @classmethod
    def random(cls):
        item = Item()
        item.value = random.randint(0, 10)
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


def create_random_items(number_of_items):
    items = []
    for count in range(0, number_of_items):
        items.append(Item.random())
    return items
