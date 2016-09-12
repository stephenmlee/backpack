class AllTestResults(object):
    def __init__(self, results=None):
        super(AllTestResults, self).__init__()
        self.results = results or {}

    def passes(self):
        return reduce(lambda passes, result: passes and result.passes, self.results.itervalues(), True)

    def lowest_bang_for_buck(self):
        return reduce(lambda least_bfb, result: result.bang_for_buck if
                      result.bang_for_buck < least_bfb else least_bfb, self.results.itervalues(), 100000000)

    def update(self, test_result):
        self.results[test_result.name] = test_result

    def for_test(self, test_name):
        try:
            return self.results[test_name]
        except KeyError:
            return None

    def copy(self):
        new_results = {}
        for test, results in self.results.iteritems():
            new_results[test] = results.copy()
        return AllTestResults(new_results)
