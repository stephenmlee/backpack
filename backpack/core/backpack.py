import random

import sys

from core.test_results import AllTestResults


class Backpack(object):
    def __init__(self, constraints=None, items=None, test_results=None):
        super(Backpack, self).__init__()
        self.items = items or []
        self.constraints = constraints or []
        self.test_results = test_results or AllTestResults()
        self.added_item = None

    def add_item(self, item):
        self.items.append(item)
        self.added_item = item

    def test(self):
        for constraint in self.constraints:
            self.test_results.update(constraint.test(self))
    
    def pack(self, target_item_count, available_items):
        backpack = self
        for item_count in range(0, target_item_count):
            sys.stdout.write('%s' % item_count)
            candidates = []
            for candidate_item in available_items:
                candidate_backpack = backpack.copy()
                candidate_backpack.add_item(candidate_item)
                candidate_backpack.test()
                if candidate_backpack.test_results.passes():
                    candidates.append(candidate_backpack)
                sys.stdout.write('.')
            sys.stdout.write('\n')
            backpack = random.choice(candidates)

        self.items = backpack.items
        self.test_results = backpack.test_results

    def copy(self):
        return Backpack(self.constraints, list(self.items), self.test_results.copy())
                
            

