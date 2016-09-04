import random

from core.testresults import TestResults


class Backpack(object):
    def __init__(self, items=None, rules=None):
        super(Backpack, self).__init__()
        self.items = items or []
        self.rules = rules or []

    def add_item(self, item):
        self.items.append(item)
        
    def add_rule(self, rule):
        self.rules.append(rule)

    def test(self):
        return TestResults()
    
    def pack(self, target_item_count, available_items):
        backpack = self
        for item_count in range(0, target_item_count):
            candidates = []
            for candidate_item in available_items:
                candidate_backpack = backpack.copy()
                candidate_backpack.add_item(candidate_item)
                candidates.append(candidate_backpack)
            backpack = random.choice(candidates)
        self.items = backpack.items

    def copy(self):
        return Backpack(list(self.items), self.rules)
                
            

