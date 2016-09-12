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
        value = self.getter_fn(item) or 0

        # Get previous results or defaults
        previous_result = backpack.test_results.for_test(self.name)
        previous_item_total = previous_result.item_total(item) if previous_result else 0
        prev_test_passed = previous_result.passes if previous_result else True

        # Calculate new total and pass/fail incrementally from previous results
        new_item_total = previous_item_total + value
        item_passed = new_item_total <= self.max_value
        test_passed = prev_test_passed and item_passed

        fit_multiple, bang_for_buck = self.calculate_bang_for_buck(new_item_total, previous_item_total, item.value)

        # Create new result object - care must be taken to replace the result dictionary (NOT just update the values)
        # as the result dictionary may not have been cloned.
        new_result = previous_result.copy() if previous_result else MaxValueResult(name=self.name)
        new_result.passes = test_passed
        new_result.update(item, {'total': new_item_total, 'pass': item_passed})
        new_result.fit_multiple = fit_multiple
        new_result.bang_for_buck = bang_for_buck
        return new_result

    def calculate_bang_for_buck(self, new_total, previous_total, value):
        delta = new_total - previous_total
        delta_pct = delta / float(self.max_value)
        previous_result_pct = previous_total / float(self.max_value)
        try:
            fit_multiple = (1 - previous_result_pct) / delta_pct
        except ZeroDivisionError:
            # Zero delta - no use of remaining limit for this item!
            fit_multiple = 1000000
        bang_for_buck = fit_multiple * value
        return fit_multiple, bang_for_buck


class MaxValueResult(object):
        def __init__(self, passes=None, results=None, name=None, fit_multiple=0, bang_for_buck=0):
            super(MaxValueResult, self).__init__()
            self.passes = passes
            self.item_results = results or {}
            self.name = name
            self.fit_multiple = fit_multiple
            self.bang_for_buck = bang_for_buck

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


