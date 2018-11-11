import re
from unittest import TextTestRunner, TextTestResult

from django.test.runner import DiscoverRunner as TestRunner

_EXPECTED_ERRORS = [
    r"This query is not supported by the database\.",
    r"Multi-table inheritance is not supported by non-relational DBs\.",
    r"TextField is not indexed, by default, so you can't filter on it\.",
    r"First ordering property must be the same as inequality filter property",
    r"This database doesn't support filtering on non-primary key ForeignKey fields\.",
    r"Only AND filters are supported\.",
    r"MultiQuery does not support keys_only\.",
    r"You can't query against more than 30 __in filter value combinations\.",
    r"Only strings and positive integers may be used as keys on GAE\.",
    r"This database does not support <class '.*'> aggregates\.",
    r"Subqueries are not supported \(yet\)\.",
    r"Cursors are not supported\.",
    r"This database backend only supports count\(\) queries on the primary key\.",
    r"AutoField \(default primary key\) values must be strings representing an ObjectId on MongoDB",
]

class ShotgunTestResult(TextTestResult):
    def __init__(self, *args, **kwargs):
        super(ShotgunTestResult, self).__init__(*args, **kwargs)
        self._compiled_exception_matchers = [re.compile(expr) for expr in _EXPECTED_ERRORS]

    def __match_exception(self, exc):
        for exc_match in self._compiled_exception_matchers:
            if exc_match.search(str(exc)):
                return True
        return False

    def addError(self, test, err):
        exc = err[1]
        if self.__match_exception(exc):
            super(ShotgunTestResult, self).addExpectedFailure(test, err)
        else:
            super(ShotgunTestResult, self).addError(test, err)


class ShotgunTestSuiteRunner(TestRunner):
    def run_suite(self, suite, **kwargs):
        return TextTestRunner(
            verbosity=self.verbosity,
            failfast=self.failfast,
            resultclass=ShotgunTestResult,
            buffer=False
        ).run(suite)

    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass



