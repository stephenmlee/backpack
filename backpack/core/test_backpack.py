from unittest import TestCase

from expecter import expect

from core.backpack import Backpack
from core.constraints import FastMaxItemValue, FastMinTotalValue
from core.item import create_random_items, Item


class TestBackpack(TestCase):
    def test_pack(self):
        target_number_of_items = 500
        items = create_random_items(500)

        constraints = [
            FastMaxItemValue(lambda x: x.weight1, 50, "Max Item Weight 1"),
            FastMaxItemValue(lambda x: x.weight2, 20, "Max Item Weight 2"),
            FastMaxItemValue(lambda x: x.weight3, 20, "Max Item Weight 3"),
            FastMaxItemValue(lambda x: x.weight4, 200, "Max Item Weight 4"),
            FastMaxItemValue(lambda x: x.weight5, 500, "Max Item Weight 5"),
        ]

        demands = [
            FastMinTotalValue(lambda x: x.weight6, 100, "Min Total Weight 6"),
            FastMinTotalValue(lambda x: x.weight7, 150, "Min Total Weight 7"),
            FastMinTotalValue(lambda x: x.weight8, 200, "Min Total Weight 8"),
            FastMinTotalValue(lambda x: x.weight9, 1000, "Min Total Weight 9"),
        ]

        backpack = Backpack(constraints, demands=demands)
        backpack.pack(target_number_of_items, items)

        expect(len(backpack.items)) == target_number_of_items

        expect(backpack.test_results.for_test("Max Item Weight 1").total) <= 50
        expect(backpack.test_results.for_test("Max Item Weight 2").total) <= 20
        expect(backpack.test_results.for_test("Max Item Weight 3").total) <= 20
        expect(backpack.test_results.for_test("Max Item Weight 4").total) <= 200
        expect(backpack.test_results.for_test("Max Item Weight 5").total) <= 500

        expect(backpack.test_results.for_test("Min Total Weight 6").total) >= 500
        expect(backpack.test_results.for_test("Min Total Weight 7").total) >= 1000
        expect(backpack.test_results.for_test("Min Total Weight 8").total) >= 2000
        expect(backpack.test_results.for_test("Min Total Weight 9").total) >= 50

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
        item2 = Item(weight1=5, value=5)
        item3 = Item(weight2=5, value=4)

        constraints = [
            FastMaxItemValue(lambda x: x.weight1, 20, "Max Item Weight 1"),
            FastMaxItemValue(lambda x: x.weight2, 20, "Max Item Weight 2"),
        ]

        backpack = Backpack(constraints)
        backpack.pack(3, [item1, item2, item3])

        expect(backpack.items) == [item2, item3, item2]

    def test_demand_heuristic_with_one_demand(self):
        item1 = Item(weight1=100, value=1)
        item2 = Item(weight1=5, value=4)
        item3 = Item(weight1=5, value=5)

        demands = [
            FastMinTotalValue(lambda x: x.weight1, 20, "Min Item Weight 1"),
        ]

        backpack = Backpack(demands=demands)
        backpack.pack(3, [item1, item2, item3])

        expect(backpack.items) == [item1,  # Top quartile progress towards demand, passes the demand minimum
                                   item3,  # No longer constrained - most bang for buck
                                   item3]  # No longer constrained - most bang for buck
