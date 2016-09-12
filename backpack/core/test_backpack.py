from unittest import TestCase

from expecter import expect

from core.backpack import Backpack
from core.constraints import FastMaxItemValue
from core.item import create_random_items


class TestBackpack(TestCase):
    def test_pack(self):
        items = create_random_items(500)

        constraints = [
            FastMaxItemValue(lambda x: x.weight1, 50, "Max Item Weight 1"),
            FastMaxItemValue(lambda x: x.weight2, 20, "Max Item Weight 2"),
            FastMaxItemValue(lambda x: x.weight3, 20, "Max Item Weight 3"),
            FastMaxItemValue(lambda x: x.weight4, 200, "Max Item Weight 4"),
            FastMaxItemValue(lambda x: x.weight5, 500, "Max Item Weight 5"),
        ]

        backpack = Backpack(constraints)
        backpack.pack(500, items)
        expect(len(backpack.items)) == 500


