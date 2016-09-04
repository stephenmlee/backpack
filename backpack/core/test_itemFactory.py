from unittest import TestCase

from expecter import expect

from backpack.core.ItemFactory import ItemFactory


class TestItemFactory(TestCase):
    def test_create_items(self):
        factory = ItemFactory()
        items = factory.create_items(500)
        expect(len(items)) == 500
