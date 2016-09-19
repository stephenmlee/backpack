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
        item.weight1 = random.uniform(1, 10)
        item.weight2 = random.uniform(1, 10)
        item.weight3 = random.uniform(1, 10)
        item.weight4 = random.uniform(1, 100)
        item.weight5 = random.uniform(1, 100)
        item.weight6 = random.uniform(1, 10)
        item.weight7 = random.uniform(1, 10)
        item.weight8 = random.uniform(1, 10)
        item.weight9 = random.uniform(1, 10)
        item.weight10 = random.uniform(78.25, 118.25)
        item.value = 10-item.weight9
        return item


def create_random_items(number_of_items):
    items = []
    for count in range(0, number_of_items):
        items.append(Item.random())
    return items
