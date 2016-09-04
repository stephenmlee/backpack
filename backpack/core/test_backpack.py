from unittest import TestCase

from expecter import expect

from core.ItemFactory import ItemFactory
from core.backpack import Backpack


class TestBackpack(TestCase):
    def test_pack(self):
        items = ItemFactory.create_items(500)
        backpack = Backpack()
        backpack.pack(500, items)
        expect(len(backpack.items)) == 500
