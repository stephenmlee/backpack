class AllTestResults(object):
    def __init__(self, constraints=None, demands=None):
        super(AllTestResults, self).__init__()
        self.constraints = constraints or {}
        self.demands = demands or {}

    def passes(self):
        return reduce(lambda passes, result: passes and result.passes, self.constraints.itervalues(), True)

    # Select the lowest bang for buck from all tests to represent the maximum potential value of the new item i.e.
    # at this point we can add at most n more of the item, multiplied by the value.
    def bang_for_buck(self):
        return reduce(lambda least_bfb, result: result.bang_for_buck if least_bfb is None or
                      result.bang_for_buck < least_bfb else least_bfb, self.constraints.itervalues(), None)

    def total_progress_to_demands(self):
        return reduce(lambda total, result: result.progress_to_demand, self.demands.itervalues(), 0)

    def update_constraint(self, test_result):
        self.constraints[test_result.name] = test_result
        self.demands.pop(test_result.name, None)

    def update_demand(self, test_result):
        self.demands[test_result.name] = test_result
        self.constraints.pop(test_result.name, None)

    def for_test(self, test_name):
        try:
            return self.constraints[test_name]
        except KeyError:
            try:
                return self.demands[test_name]
            except KeyError:
                return None

    def copy(self):
        new_constraints = {}
        new_demands = {}

        for test, results in self.constraints.iteritems():
            new_constraints[test] = results.copy()
        for test, results in self.demands.iteritems():
            new_demands[test] = results.copy()

        return AllTestResults(new_constraints, new_demands)

    def __str__(self):
        formatted = ""
        for test_name, test_result in sorted(list(self.constraints.iteritems()) + list(self.demands.iteritems())):
            formatted += ":%f" % test_result.total_pct
        return formatted


