"""
Functional tests: Verify the SimpleApp console application runs and produces correct output.

Validates that:
- SimpleApp.exe starts and produces output
- Calculator operations display correct results for the hardcoded inputs (a=10, b=5)
- The welcome banner is present
- All four arithmetic operations appear in the output
"""
import os
import subprocess
import pytest

WORKSPACE_DIR = os.environ.get("WORKSPACE_DIR", "/l2l/workspace")
REPO_DIR = os.path.join(WORKSPACE_DIR, "dotnet-4-5")
SIMPLEAPP_EXE = os.path.join(REPO_DIR, "bin", "Debug", "SimpleApp.exe")


@pytest.fixture(scope="module")
def app_output():
    """Run SimpleApp.exe with piped stdin and capture output.

    The app calls Console.ReadKey() which throws when stdin is redirected,
    but output before that call is still captured.
    """
    assert os.path.isfile(SIMPLEAPP_EXE), f"SimpleApp.exe not found at {SIMPLEAPP_EXE}"

    result = subprocess.run(
        [SIMPLEAPP_EXE],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
        timeout=30,
        input="",
    )
    # App will exit non-zero due to Console.ReadKey() exception when stdin is piped.
    # That is expected. We care about the stdout content before the crash.
    return result


class TestConsoleAppOutput:
    """Verify console application prints correct calculator results."""

    def test_app_produces_output(self, app_output):
        """SimpleApp.exe writes something to stdout."""
        assert len(app_output.stdout) > 0, "App produced no stdout"

    def test_welcome_banner(self, app_output):
        """Output starts with the welcome banner."""
        assert "Welcome to SimpleApp!" in app_output.stdout
        assert "======================" in app_output.stdout

    def test_displays_operands(self, app_output):
        """Output shows the operands used (10 and 5)."""
        assert "Calculating with numbers: 10 and 5" in app_output.stdout

    def test_addition_result(self, app_output):
        """Addition: 10 + 5 = 15."""
        assert "Addition: 15" in app_output.stdout

    def test_subtraction_result(self, app_output):
        """Subtraction: 10 - 5 = 5."""
        assert "Subtraction: 5" in app_output.stdout

    def test_multiplication_result(self, app_output):
        """Multiplication: 10 * 5 = 50."""
        assert "Multiplication: 50" in app_output.stdout

    def test_division_result(self, app_output):
        """Division: 10 / 5 = 2."""
        assert "Division: 2" in app_output.stdout
