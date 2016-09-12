from unittest import TestCase

from expecter import expect

from core.backpack import Backpack
from core.constraints import FastMaxItemValue
from core.item import create_random_items, Item


class TestBackpack(TestCase):
    def test_pack(self):
        target_number_of_items = 10
        items = create_random_items(500)

        constraints = [
            FastMaxItemValue(lambda x: x.weight1, 50, "Max Item Weight 1"),
            FastMaxItemValue(lambda x: x.weight2, 20, "Max Item Weight 2"),
            FastMaxItemValue(lambda x: x.weight3, 20, "Max Item Weight 3"),
            FastMaxItemValue(lambda x: x.weight4, 200, "Max Item Weight 4"),
            FastMaxItemValue(lambda x: x.weight5, 500, "Max Item Weight 5"),
        ]

        backpack = Backpack(constraints)
        backpack.pack(target_number_of_items, items)
        expect(len(backpack.items)) == target_number_of_items

    def test_constraint_heuristic_with_one_constraint(self):
        item1 = Item(weight1=100, value=1)
        item2 = Item(weight1=5, value=4)
        item3 = Item(weight1=5, value=5)

        constraints = [
            FastMaxItemValue(lambda x: x.weight1, 20, "Max Item Weight 1"),
        ]

        backpack = Backpack(constraints)
        backpack.pack(3, [item1, item2, item3])

        expect(backpack.items) == [item3, item2, item3]

    def test_constraint_heuristic_with_two_constraints(self):
        item1 = Item(weight1=100, value=1)
        item2 = Item(weight2=5, value=4)
        item3 = Item(weight1=5, value=5)

        constraints = [
            FastMaxItemValue(lambda x: x.weight1, 20, "Max Item Weight 1"),
            FastMaxItemValue(lambda x: x.weight2, 20, "Max Item Weight 2"),
        ]

        backpack = Backpack(constraints)
        backpack.pack(3, [item1, item2, item3])

        expect(backpack.items) == [item3, item2, item3]
