from collections import defaultdict


# A single type of item can take up to the specified value in the given weight
class MaxItemValue(object):
    name = "Max Item Value"

    def __init__(self, getter_fn, max_value):
        self.getter_fn = getter_fn
        self.max_value = max_value

    def test(self, backpack):
        totals, backpack_total = self._compute_totals(backpack)
        return self._calculate_results(totals)

    def _calculate_results(self, totals):
        results = {}
        passed = True
        for item, item_total in totals.iteritems():
            item_passed = item_total <= self.max_value
            passed = passed and item_passed
            results[item] = {'total': item_total, 'pass': item_passed}
        return MaxValueResults(passed, results, self.name)

    def _compute_totals(self, backpack):
        totals = defaultdict(float)
        total_sum = 0
        for item in backpack.items:
            value = self.getter_fn(item)
            total_sum += value
            totals[item] += value
        return totals, max(total_sum, 100)


# Similar to MaxItemValue but uses previous test results to incrementally calculate the new total for a single item
# instead of summing over all items in the backpack
class FastMaxItemValue(object):
    def __init__(self, getter_fn, max_value, name):
        self.getter_fn = getter_fn
        self.max_value = max_value
        self.name = name

    def test(self, backpack):
        previous_results = backpack.test_results.for_test(self.name)
        item = backpack.added_item
        prev_item_result = previous_results.get(item) if previous_results else None

        if prev_item_result:
            new_total = prev_item_result['total'] + self.getter_fn(item)
            item_passed = new_total <= self.max_value
            test_passed = prev_item_result['pass'] and item_passed

            all_item_results = previous_results.item_results
            all_item_results[item] = {'total': new_total, 'pass': item_passed}
        else:
            value = self.getter_fn(item)
            item_passed = value <= self.max_value
            test_passed = item_passed
            all_item_results = previous_results.item_results if previous_results else {}
            all_item_results[item] = {'total': value, 'pass': item_passed}

        return MaxValueResults(test_passed, all_item_results, self.name)


class MaxValueResults(object):
        def __init__(self, passes, results, name):
            super(MaxValueResults, self).__init__()
            self.passes = passes
            self.item_results = results
            self.name = name

        def get(self, item):
            return self.item_results.get(item)

        def copy(self):
            return MaxValueResults(self.passes, self.item_results.copy(), self.name)


