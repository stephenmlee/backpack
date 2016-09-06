import random

from core.test_results import TestResults


class Backpack(object):
    def __init__(self, constraints=None, items=None, ):
        super(Backpack, self).__init__()
        self.items = items or []
        self.constraints = constraints or []

    def add_item(self, item):
        self.items.append(item)

    def test(self):
        for constraint in self.constraints:
            TestResults.add(constraint.test(self))
        return TestResults()
    
    def pack(self, target_item_count, available_items):
        backpack = self
        for item_count in range(0, target_item_count):
            print item_count
            candidates = []
            for candidate_item in available_items:
                candidate_backpack = backpack.copy()
                candidate_backpack.add_item(candidate_item)
                test_results = candidate_backpack.test()
                if test_results.passes():
                    candidates.append(candidate_backpack)
            backpack = random.choice(candidates)
        self.items = backpack.items

    def copy(self):
        return Backpack(self.constraints, list(self.items))
                
            

