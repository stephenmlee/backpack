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
        return MaxValueResult(passed, results, self.name)

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
        item = backpack.added_item
        value = self.getter_fn(item)

        # Get previous results or defaults
        previous_result = backpack.test_results.for_test(self.name)
        previous_item_total = previous_result.item_total(item) if previous_result else 0
        prev_test_passed = previous_result.passes if previous_result else True

        # Calculate new total and pass/fail incrementally from previous results
        new_total = previous_item_total + value
        item_passed = new_total <= self.max_value
        test_passed = prev_test_passed and item_passed

        # Create new result object - care must be taken to replace the result dictionary (NOT just update the values)
        # as the result dictionary may not have been cloned.
        new_result = previous_result.copy() if previous_result else MaxValueResult(name=self.name)
        new_result.passes = test_passed
        new_result.update(item, {'total': new_total, 'pass': item_passed})
        return new_result


class MaxValueResult(object):
        def __init__(self, passes=None, results=None, name=None):
            super(MaxValueResult, self).__init__()
            self.passes = passes
            self.item_results = results or {}
            self.name = name

        def update(self, item, result):
            self.item_results[item] = result

        def item_total(self, item):
            try:
                return self.item_results[item]['total']
            except KeyError:
                return 0

        def item_passed(self, item):
            try:
                return self.item_results[item]['passed']
            except KeyError:
                return True

        def copy(self):
            return MaxValueResult(self.passes, self.item_results.copy(), self.name)


