import random

import sys

from core.test_results import AllTestResults


class Backpack(object):
    def __init__(self, constraints=None, items=None, test_results=None, demands=None, target_item_count=None):
        super(Backpack, self).__init__()
        self.items = items or []
        self.constraints = constraints or []
        self.demands = demands or []
        self.test_results = test_results or AllTestResults()
        self.added_item = None
        self.target_item_count = target_item_count

    def add_item(self, item):
        self.items.append(item)
        self.added_item = item

    def pack(self, target_item_count, available_items):
        backpack = self
        backpack.target_item_count = target_item_count
        print self.headers()
        for item_count in range(0, target_item_count):
            candidates = []
            for candidate_item in available_items:
                candidate_backpack = backpack.copy()
                candidate_backpack.add_item(candidate_item)
                candidate_backpack.test()
                if candidate_backpack.test_results.passes():
                    candidates.append(candidate_backpack)

            backpack = self.apply_selection_heuristic(candidates)
            backpack.turn_passing_demands_into_constraints()

            print "%s%s:%s" % (item_count, backpack.test_results, backpack.added_item.weight10)

        self.items = backpack.items
        self.test_results = backpack.test_results

    def test(self):
        for constraint in self.constraints:
            self.test_results.update_constraint(constraint.test(self))
        for demand in self.demands:
            self.test_results.update_demand(demand.test(self))

    def apply_selection_heuristic(self, candidates):
        if len(candidates) == 0:
            raise Exception("No candidates to choose from")

        if len(self.demands) > 0:
            # Pick the top quartile of candidates based on progress towards demands
            candidates.sort(key=lambda x: x.test_results.total_progress_to_demands(), reverse=True)
            candidates = candidates[:len(candidates)/4 + 1]

        candidates.sort(key=lambda x: x.test_results.bang_for_buck(), reverse=True)
        return candidates[0]

    def turn_passing_demands_into_constraints(self):
        passing_demands = []
        for demand_result in self.test_results.demands.itervalues():
            if demand_result.passes:
                passing_demands.append(demand_result)

        for demand_result in passing_demands:
            self.test_results.demands.pop(demand_result.name)
            self.test_results.constraints[demand_result.name] = demand_result
            self.demands.remove(demand_result.rule)
            self.constraints.append(demand_result.rule)

    def copy(self):
        return Backpack(self.constraints, list(self.items), self.test_results.copy(), self.demands,
                        self.target_item_count)

    def headers(self):
        formatted = "Backpack"
        for rule in sorted(self.constraints + self.demands, key=lambda x: x.name):
            formatted += ":%s" % rule.name
        formatted += ":%s" % "Weight 10"
        return formatted

            

