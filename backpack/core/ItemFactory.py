import random

from backpack.core.item import Item


class ItemFactory(object):

    def create_items(self, number_of_items):
        items = []
        for count in range(0, number_of_items):
            items.append(Item.random())
        return items


