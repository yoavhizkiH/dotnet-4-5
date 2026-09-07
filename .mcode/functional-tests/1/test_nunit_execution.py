"""
Functional tests: Verify NUnit test runner executes all tests successfully.

Validates that:
- nunit3-console.exe can run the test assembly
- All 42 test cases pass
- No tests fail, are skipped, or are inconclusive
- Test results contain expected categories (Add, Subtract, Multiply, Divide)
"""
import os
import re
import subprocess
import pytest

WORKSPACE_DIR = os.environ.get("WORKSPACE_DIR", "/l2l/workspace")
REPO_DIR = os.path.join(WORKSPACE_DIR, "dotnet-4-5")
TEST_DLL = os.path.join(REPO_DIR, "SimpleApp.Tests", "bin", "Debug", "SimpleApp.Tests.dll")
NUNIT_CONSOLE = "nunit3-console"


@pytest.fixture(scope="module")
def nunit_result():
    """Run NUnit test suite once and return the result for all tests in module."""
    assert os.path.isfile(TEST_DLL), f"Test DLL not found at {TEST_DLL}"

    result = subprocess.run(
        [NUNIT_CONSOLE, TEST_DLL, "--noresult"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
        timeout=120,
    )
    return result


class TestNUnitOverallExecution:
    """Verify nunit3-console runs the full test suite."""

    def test_nunit_runner_exits_zero(self, nunit_result):
        """nunit3-console exits with code 0 (all tests pass)."""
        assert nunit_result.returncode == 0, (
            f"nunit3-console exited with code {nunit_result.returncode}\n"
            f"stdout: {nunit_result.stdout}\nstderr: {nunit_result.stderr}"
        )

    def test_overall_result_is_passed(self, nunit_result):
        """Test run summary shows 'Overall result: Passed'."""
        assert "Overall result: Passed" in nunit_result.stdout, (
            f"Expected 'Overall result: Passed' in output:\n{nunit_result.stdout}"
        )

    def test_total_test_count_is_42(self, nunit_result):
        """Test Count is exactly 42."""
        match = re.search(r"Test Count:\s*(\d+)", nunit_result.stdout)
        assert match is not None, f"Could not find 'Test Count' in output:\n{nunit_result.stdout}"
        count = int(match.group(1))
        assert count == 42, f"Expected 42 tests, found {count}"

    def test_all_tests_passed(self, nunit_result):
        """Passed count equals total test count (42)."""
        match = re.search(r"Passed:\s*(\d+)", nunit_result.stdout)
        assert match is not None, f"Could not find 'Passed' count in output:\n{nunit_result.stdout}"
        passed = int(match.group(1))
        assert passed == 42, f"Expected 42 passed, got {passed}"

    def test_zero_failures(self, nunit_result):
        """No test failures."""
        match = re.search(r"Failed:\s*(\d+)", nunit_result.stdout)
        assert match is not None, f"Could not find 'Failed' count in output:\n{nunit_result.stdout}"
        failed = int(match.group(1))
        assert failed == 0, f"Expected 0 failures, got {failed}"

    def test_zero_skipped(self, nunit_result):
        """No tests skipped."""
        match = re.search(r"Skipped:\s*(\d+)", nunit_result.stdout)
        assert match is not None, f"Could not find 'Skipped' count in output:\n{nunit_result.stdout}"
        skipped = int(match.group(1))
        assert skipped == 0, f"Expected 0 skipped, got {skipped}"

    def test_zero_inconclusive(self, nunit_result):
        """No inconclusive tests."""
        match = re.search(r"Inconclusive:\s*(\d+)", nunit_result.stdout)
        assert match is not None, (
            f"Could not find 'Inconclusive' count in output:\n{nunit_result.stdout}"
        )
        inconclusive = int(match.group(1))
        assert inconclusive == 0, f"Expected 0 inconclusive, got {inconclusive}"


class TestNUnitFilteredExecution:
    """Verify specific test categories run and pass via NUnit filter."""

    def test_add_tests_pass(self):
        """Add operation tests pass when filtered by name."""
        result = subprocess.run(
            [NUNIT_CONSOLE, TEST_DLL, "--noresult", "--where", "method =~ /Add/"],
            cwd=REPO_DIR,
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result.returncode == 0, (
            f"Add tests failed (exit {result.returncode}):\n{result.stdout}\n{result.stderr}"
        )
        assert "Overall result: Passed" in result.stdout

    def test_subtract_tests_pass(self):
        """Subtract operation tests pass when filtered by name."""
        result = subprocess.run(
            [NUNIT_CONSOLE, TEST_DLL, "--noresult", "--where", "method =~ /Subtract/"],
            cwd=REPO_DIR,
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result.returncode == 0, (
            f"Subtract tests failed (exit {result.returncode}):\n{result.stdout}\n{result.stderr}"
        )
        assert "Overall result: Passed" in result.stdout

    def test_multiply_tests_pass(self):
        """Multiply operation tests pass when filtered by name."""
        result = subprocess.run(
            [NUNIT_CONSOLE, TEST_DLL, "--noresult", "--where", "method =~ /Multiply/"],
            cwd=REPO_DIR,
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result.returncode == 0, (
            f"Multiply tests failed (exit {result.returncode}):\n{result.stdout}\n{result.stderr}"
        )
        assert "Overall result: Passed" in result.stdout

    def test_divide_tests_pass(self):
        """Divide operation tests pass when filtered by name."""
        result = subprocess.run(
            [NUNIT_CONSOLE, TEST_DLL, "--noresult", "--where", "method =~ /Divide/"],
            cwd=REPO_DIR,
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result.returncode == 0, (
            f"Divide tests failed (exit {result.returncode}):\n{result.stdout}\n{result.stderr}"
        )
        assert "Overall result: Passed" in result.stdout

    def test_add_test_count(self):
        """Add operation has expected number of test cases (9: 7 basic + 2 overflow)."""
        result = subprocess.run(
            [NUNIT_CONSOLE, TEST_DLL, "--noresult", "--where", "method =~ /Add/"],
            cwd=REPO_DIR,
            capture_output=True,
            text=True,
            timeout=60,
        )
        match = re.search(r"Test Count:\s*(\d+)", result.stdout)
        assert match is not None, f"Could not find test count in:\n{result.stdout}"
        count = int(match.group(1))
        assert count == 9, f"Expected 9 Add tests, got {count}"

    def test_subtract_test_count(self):
        """Subtract operation has expected number of test cases (9: 7 basic + 2 overflow)."""
        result = subprocess.run(
            [NUNIT_CONSOLE, TEST_DLL, "--noresult", "--where", "method =~ /Subtract/"],
            cwd=REPO_DIR,
            capture_output=True,
            text=True,
            timeout=60,
        )
        match = re.search(r"Test Count:\s*(\d+)", result.stdout)
        assert match is not None, f"Could not find test count in:\n{result.stdout}"
        count = int(match.group(1))
        assert count == 9, f"Expected 9 Subtract tests, got {count}"

    def test_multiply_test_count(self):
        """Multiply operation has expected number of test cases (9: 7 basic + 2 overflow)."""
        result = subprocess.run(
            [NUNIT_CONSOLE, TEST_DLL, "--noresult", "--where", "method =~ /Multiply/"],
            cwd=REPO_DIR,
            capture_output=True,
            text=True,
            timeout=60,
        )
        match = re.search(r"Test Count:\s*(\d+)", result.stdout)
        assert match is not None, f"Could not find test count in:\n{result.stdout}"
        count = int(match.group(1))
        assert count == 9, f"Expected 9 Multiply tests, got {count}"

    def test_divide_test_count(self):
        """Divide operation has expected number of test cases (15: 6 basic + 4 boundary + 1 repeating + 3 exception + 1 same-value)."""
        result = subprocess.run(
            [NUNIT_CONSOLE, TEST_DLL, "--noresult", "--where", "method =~ /Divide/"],
            cwd=REPO_DIR,
            capture_output=True,
            text=True,
            timeout=60,
        )
        match = re.search(r"Test Count:\s*(\d+)", result.stdout)
        assert match is not None, f"Could not find test count in:\n{result.stdout}"
        count = int(match.group(1))
        assert count == 15, f"Expected 15 Divide tests, got {count}"
