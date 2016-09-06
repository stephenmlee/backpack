from unittest import TestCase

from expecter import expect

from core.backpack import Backpack
from core.constraints import MaxItemValue
from core.item import create_random_items


class TestBackpack(TestCase):
    def test_pack(self):
        items = create_random_items(500)

        constraints = [
            MaxItemValue(lambda x: x.weight1, 50),
            MaxItemValue(lambda x: x.weight2, 20),
            MaxItemValue(lambda x: x.weight3, 20),
            MaxItemValue(lambda x: x.weight4, 200),
            MaxItemValue(lambda x: x.weight5, 500),
        ]

        backpack = Backpack(constraints)
        backpack.pack(500, items)
        expect(len(backpack.items)) == 500
