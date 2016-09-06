from unittest import TestCase

from expecter import expect

from core.backpack import Backpack
from core.constraints import MaxItemValue
from core.item import Item


class TestMaxItemValue(TestCase):
    def test_passes(self):
        backpack = Backpack(items=[self.create_item(10)])
        constraint = MaxItemValue(lambda x: x.weight1, 10)
        results = constraint.test(backpack)
        expect(results.passed) == True

    def test_fails(self):
        item2 = self.create_item(25.1)
        backpack = Backpack(items=[self.create_item(50), item2, item2])
        constraint = MaxItemValue(lambda x: x.weight1, 50)
        results = constraint.test(backpack)
        expect(results.passed) == False

    def create_item(self, weight1_value):
        item = Item()
        item.weight1 = weight1_value
        return item

