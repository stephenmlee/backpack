from unittest import TestCase

from expecter import expect

from core.backpack import Backpack
from core.constraints import MaxItemValue, FastMaxItemValue, MaxValueResults
from core.item import Item
from core.test_results import AllTestResults


class TestMaxItemValue(TestCase):
    def test_passes(self):
        backpack = Backpack(items=[Item(weight1=10)])
        constraint = MaxItemValue(lambda x: x.weight1, 10)
        results = constraint.test(backpack)
        expect(results.passes) == True

    def test_fails(self):
        item2 = Item(weight1=25.1)
        backpack = Backpack(items=[Item(weight1=50), item2, item2])
        constraint = MaxItemValue(lambda x: x.weight1, 50)
        results = constraint.test(backpack)
        expect(results.passes) == False


class TestFastMaxItemValue(TestCase):
    def test_passes(self):
        backpack = Backpack()
        backpack.add_item(Item(weight1=10))
        constraint = FastMaxItemValue(lambda x: x.weight1, 10, "Test Rule")
        results = constraint.test(backpack)
        expect(results.passes) == True

    def test_fails(self):
        item = Item(weight1=25.1)
        max_value_results = MaxValueResults(True, {item: {'pass': True, 'total': 25.1}}, "Test Rule")
        results = AllTestResults()
        results.add(max_value_results)

        backpack = Backpack(test_results=results)
        backpack.add_item(item)

        constraint = FastMaxItemValue(lambda x: x.weight1, 50, "Test Rule")
        new_max_value_results = constraint.test(backpack)
        expect(new_max_value_results.passes) == False

