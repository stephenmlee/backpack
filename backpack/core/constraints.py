from collections import defaultdict


# A single type of item can take up to the specified value in the given weight
class MaxItemValue(object):
    def __init__(self, getter_fn, max_value):
        self.getter_fn = getter_fn
        self.max_value = max_value

    def test(self, backpack):
        totals, backpack_total = self._compute_totals(backpack)
        return self._calculate_results(totals)

    def _calculate_results(self, totals):
        results = []
        passed = True
        for item, item_total in totals.iteritems():
            item_passed = item_total <= self.max_value
            passed = passed and item_passed
            results.append({'item': item, 'result': item_total, 'pass': item_passed})
        return MaxValueResults(passed, results)

    def _compute_totals(self, backpack):
        totals = defaultdict(float)
        total_sum = 0
        for item in backpack.items:
            value = self.getter_fn(item)
            total_sum += value
            totals[item] += value
        return totals, max(total_sum, 100)


class MaxValueResults(object):
        def __init__(self, passed, results):
            super(MaxValueResults, self).__init__()
            self.passed = passed
            self.results = results


