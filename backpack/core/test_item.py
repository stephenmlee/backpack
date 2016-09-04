from unittest import TestCase

from expecter import expect

from core.item import create_random_items


class TestItem(TestCase):
    def test_create_items(self):
        items = create_random_items(500)
        expect(len(items)) == 500
        0 <= expect(items[0].weight1) <= 10
        0 <= expect(items[0].weight2) <= 10
        0 <= expect(items[0].weight3) <= 10
        0 <= expect(items[0].weight4) <= 100
        0 <= expect(items[0].weight5) <= 100
        0 <= expect(items[0].weight6) <= 100
        0 <= expect(items[0].weight7) <= 1000
        0 <= expect(items[0].weight8) <= 1000
        0 <= expect(items[0].weight9) <= 1000
        0 <= expect(items[0].weight10) <= 1
