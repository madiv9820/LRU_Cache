"""
🧭 This test file turns every JSON test case into its own unittest so each
LRU Cache scenario gets clear pass/fail reporting, along with a timeout guard.

Each case contains a sequence of cache operations such as `put` and `get`.
The Solution class executes the complete operation sequence, while this
runner focuses only on loading cases, validating results, and reporting
test outcomes.
"""

import json
import os
import time
import unittest
from typing import Any, Dict, List
from timeout_decorator import TimeoutError, timeout
from source.solution import Solution


def _to_test_name(title: str) -> str:
    # 🏷️ Convert each friendly title into a safe unittest method name.
    sanitized = ''.join(
        char.lower() if char.isalnum() else '_'
        for char in title
    )

    compact = '_'.join(
        part for part in sanitized.split('_')
        if part
    )

    return f'test_{compact}'


def _make_testcase(testcase: Dict[str, Any]):
    # 🧱 Build one real unittest method for every JSON test case.
    def test_method(self):
        title: str = testcase['title']
        operations: List[str] = testcase['input'][0]
        values: List[List[int]] = testcase['input'][1]
        expected_output: List[Any] = testcase['output']
        description: str = testcase.get(
            'description',
            'No description provided.'
        )

        self._case_title = title
        self._case_description = description

        print('\n' + '=' * 60)
        print(f'🧪 Test Case : {title}')
        print(f'🤔 Scenario  : {description}')
        print(f'📝 Operations: {operations}')
        print(f'📦 Values    : {values}')
        print('⏳ Starting soon...')

        time.sleep(self.DISPLAY_DELAY_SECONDS)

        try:
            actual_output: List[Any] = self._run_case(
                operations=operations,
                values=values
            )

        except TimeoutError:
            print(f'⏱️ Result    : Time Limit Exceeded in {title}')
            print('=' * 60)

            self.fail(
                f'⏱️ Time Limit Exceeded: {title}'
            )

        if actual_output == expected_output:
            print(
                f'✅ Result    : Passed with answer {actual_output}'
            )
        else:
            print(
                f'❌ Result    : Expected {expected_output}, '
                f'got {actual_output}'
            )

        print('=' * 60)

        time.sleep(self.DISPLAY_DELAY_SECONDS)

        self.assertEqual(
            actual_output,
            expected_output,
            f'❌ Value Mismatch in {title}\n'
            f'Expected = {expected_output}\n'
            f'Actual   = {actual_output}'
        )

    return test_method


class TestSolution(unittest.TestCase):
    # 🎛️ Adjust this to make the test run faster or more cinematic.
    DISPLAY_DELAY_SECONDS = 2

    # 🧾 Store the result of every individual test case.
    CASE_RESULTS: List[Dict[str, str]] = []

    def setUp(self):
        # 🛠️ Create a fresh Solution instance for every test case.
        self.__solution = Solution()

        return super().setUp()

    @timeout(1)
    def _run_case(
        self,
        operations: List[str],
        values: List[List[int]]
    ) -> List[Any]:
        # ⚡ Give every test case its own timeout.
        return self.__solution.execute(
            operations=operations,
            values=values
        )


class LRUCacheTestResult(unittest.TextTestResult):
    # 🧾 Capture every testcase outcome for the final summary.

    def addSuccess(self, test):
        super().addSuccess(test)

        TestSolution.CASE_RESULTS.append(
            {
                'title': getattr(
                    test,
                    '_case_title',
                    test._testMethodName
                ),
                'status': '✅ Passed',
            }
        )

    def addFailure(self, test, err):
        super().addFailure(test, err)

        TestSolution.CASE_RESULTS.append(
            {
                'title': getattr(
                    test,
                    '_case_title',
                    test._testMethodName
                ),
                'status': '❌ Failed',
            }
        )

    def addError(self, test, err):
        super().addError(test, err)

        TestSolution.CASE_RESULTS.append(
            {
                'title': getattr(
                    test,
                    '_case_title',
                    test._testMethodName
                ),
                'status': '💥 Error',
            }
        )

    def stopTestRun(self):
        super().stopTestRun()

        print('\n' + '🧾' + '=' * 58)
        print('📚 LRU Cache Final Summary')

        if not TestSolution.CASE_RESULTS:
            print('No test cases were executed.')
            print('=' * 60)
            return

        passed_count = sum(
            result['status'] == '✅ Passed'
            for result in TestSolution.CASE_RESULTS
        )

        failed_count = sum(
            result['status'] == '❌ Failed'
            for result in TestSolution.CASE_RESULTS
        )

        error_count = sum(
            result['status'] == '💥 Error'
            for result in TestSolution.CASE_RESULTS
        )

        total_count = len(TestSolution.CASE_RESULTS)

        success_rate = (
            passed_count / total_count
        ) * 100

        title_width = max(
            len('Test Case'),
            *(
                len(result['title'])
                for result in TestSolution.CASE_RESULTS
            )
        )

        status_width = max(
            len('Status'),
            *(
                len(result['status'])
                for result in TestSolution.CASE_RESULTS
            )
        )

        divider = (
            f"+-{'-' * title_width}"
            f"-+-{'-' * status_width}-+"
        )

        header = (
            f"| {'Test Case'.ljust(title_width)} "
            f"| {'Status'.ljust(status_width)} |"
        )

        print(divider)
        print(header)
        print(divider)

        for result in TestSolution.CASE_RESULTS:
            print(
                f"| {result['title'].ljust(title_width)} "
                f"| {result['status'].ljust(status_width)} |"
            )

        print(divider)

        print(
            f'🏁 Total: {total_count} | '
            f'✅ Passed: {passed_count} | '
            f'❌ Failed: {failed_count} | '
            f'💥 Errors: {error_count}'
        )

        print(f'📈 Success Rate: {success_rate:.2f}%')
        print('=' * 60)


# 📂 Locate the JSON test-case file relative to this test file.
_CURRENT_DIRECTORY = os.path.dirname(
    os.path.abspath(__file__)
)

_FILE_PATH = os.path.join(
    _CURRENT_DIRECTORY,
    'cases.json'
)


# 📖 Load all test cases and dynamically register them with unittest.
with open(
    _FILE_PATH,
    mode='r',
    encoding='utf-8'
) as read_file:

    all_testcases = json.load(read_file)

    # 🧪 Register every JSON case as a standalone unittest.
    for testcase in all_testcases:
        setattr(
            TestSolution,
            _to_test_name(testcase['title']),
            _make_testcase(testcase)
        )


if __name__ == '__main__':
    unittest.main(
        verbosity=2,
        testRunner=unittest.TextTestRunner(
            resultclass=LRUCacheTestResult
        )
    )