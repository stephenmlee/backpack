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
        self.limit = float(max_value)
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
        item_passed = new_item_total <= self.limit
        test_passed = prev_test_passed and item_passed

        fit_multiple, bang_for_buck = self.calculate_bang_for_buck(new_item_total, previous_item_total, item.value)

        # Create new result object - care must be taken to replace the result dictionary (NOT just update the values)
        # as the result dictionary may not have been cloned.
        new_result = previous_result.copy() if previous_result else MaxValueResult(name=self.name)
        new_result.passes = test_passed
        new_result.update(item, {'total': new_item_total, 'result': new_item_total / self.limit, 'pass': item_passed})
        new_result.fit_multiple = fit_multiple
        new_result.bang_for_buck = bang_for_buck
        return new_result

    def calculate_bang_for_buck(self, new_result, previous_result, value):
        delta = new_result - previous_result
        try:
            fit_multiple = (self.limit - previous_result) / delta
        except ZeroDivisionError:
            # Zero delta - no consumption of remaining capacity for this item! Give it a huge fit multiple as reward.
            fit_multiple = 1000000000
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

        @property
        def total(self):
            return reduce(lambda max, item_result: item_result['total'] if item_result['total'] > max else max,
                          self.item_results.itervalues(), 0)

        @property
        def result(self):
            return reduce(lambda max, item_result: item_result['result'] if item_result['result'] > max else max,
                          self.item_results.itervalues(), 0)

        def copy(self):
            return MaxValueResult(self.passes, self.item_results.copy(), self.name)


class FastMinTotalValue(object):
    def __init__(self, getter_fn, min_value, name):
        self.getter_fn = getter_fn
        self.minimum = float(min_value)
        self.name = name

    def test(self, backpack):
        item = backpack.added_item
        weight = self.getter_fn(item) or 0

        # Get previous results or defaults
        previous_result = backpack.test_results.for_test(self.name)
        previous_total = previous_result.total if previous_result else 0

        # Calculate new total and pass/fail incrementally from previous results
        new_total = previous_total + weight
        passes = new_total >= self.minimum
        progress_to_demand = weight / self.minimum
        bang_for_buck = 1000000000 * item.value

        return MinTotalValueResult(passes, new_total, progress_to_demand, self, bang_for_buck, new_total / self.minimum)


class MinTotalValueResult(object):
    def __init__(self, passes, total, progress_to_demand, rule, bang_for_buck, result):
        super(MinTotalValueResult, self).__init__()
        self.passes = passes
        self.total = total
        self.result = result
        self.progress_to_demand = progress_to_demand or 0
        self.name = rule.name
        self.rule = rule
        self.bang_for_buck = bang_for_buck

    def copy(self):
        return MinTotalValueResult(self.passes, self.total, self.progress_to_demand, self.rule, self.bang_for_buck, self.result)
