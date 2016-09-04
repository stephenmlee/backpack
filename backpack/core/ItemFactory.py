from core.item import Item


class ItemFactory(object):

    @classmethod
    def create_items(cls, number_of_items):
        items = []
        for count in range(0, number_of_items):
            items.append(Item.random())
        return items
