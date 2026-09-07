"""
Functional tests: Verify that both SimpleApp and SimpleApp.Tests build successfully.

Validates that:
- MSBuild compiles SimpleApp.csproj producing SimpleApp.exe
- MSBuild compiles SimpleApp.Tests.csproj producing SimpleApp.Tests.dll
- Build artifacts exist at expected locations
- Build completes without errors (warnings are acceptable)
"""
import os
import subprocess
import pytest

WORKSPACE_DIR = os.environ.get("WORKSPACE_DIR", "/l2l/workspace")
REPO_DIR = os.path.join(WORKSPACE_DIR, "dotnet-4-5")
MSBUILD = r"C:\Windows\Microsoft.NET\Framework64\v4.0.30319\MSBuild.exe"


def get_csc_tool_path():
    """Find the Roslyn compiler path from Microsoft.Net.Compilers package."""
    packages_dir = os.path.join(REPO_DIR, "packages")
    for entry in os.listdir(packages_dir):
        if entry.lower().startswith("microsoft.net.compilers"):
            tools_path = os.path.join(packages_dir, entry, "tools")
            if os.path.isdir(tools_path):
                return tools_path
    return None


class TestSourceProjectBuild:
    """Verify SimpleApp.csproj builds to produce SimpleApp.exe."""

    def test_source_project_builds_successfully(self):
        """MSBuild compiles SimpleApp.csproj without errors."""
        csc_path = get_csc_tool_path()
        assert csc_path is not None, "Microsoft.Net.Compilers tools directory not found"

        result = subprocess.run(
            [
                MSBUILD,
                "SimpleApp.csproj",
                "/p:Configuration=Debug",
                f"/p:CscToolPath={csc_path}",
                "/t:Build",
                "/verbosity:minimal",
            ],
            cwd=REPO_DIR,
            capture_output=True,
            text=True,
            timeout=120,
        )
        assert result.returncode == 0, f"Build failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"

    def test_source_exe_artifact_exists(self):
        """SimpleApp.exe exists in bin/Debug after build."""
        exe_path = os.path.join(REPO_DIR, "bin", "Debug", "SimpleApp.exe")
        assert os.path.isfile(exe_path), f"SimpleApp.exe not found at {exe_path}"

    def test_source_exe_is_nonempty(self):
        """SimpleApp.exe is a non-empty file."""
        exe_path = os.path.join(REPO_DIR, "bin", "Debug", "SimpleApp.exe")
        assert os.path.isfile(exe_path), f"SimpleApp.exe not found at {exe_path}"
        size = os.path.getsize(exe_path)
        assert size > 0, f"SimpleApp.exe is empty (size={size})"


class TestTestProjectBuild:
    """Verify SimpleApp.Tests.csproj builds to produce SimpleApp.Tests.dll."""

    def test_test_project_builds_successfully(self):
        """MSBuild compiles SimpleApp.Tests.csproj without errors."""
        csc_path = get_csc_tool_path()
        assert csc_path is not None, "Microsoft.Net.Compilers tools directory not found"

        result = subprocess.run(
            [
                MSBUILD,
                os.path.join("SimpleApp.Tests", "SimpleApp.Tests.csproj"),
                "/p:Configuration=Debug",
                f"/p:CscToolPath={csc_path}",
                "/t:Build",
                "/verbosity:minimal",
            ],
            cwd=REPO_DIR,
            capture_output=True,
            text=True,
            timeout=120,
        )
        assert result.returncode == 0, f"Build failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"

    def test_test_dll_artifact_exists(self):
        """SimpleApp.Tests.dll exists in SimpleApp.Tests/bin/Debug after build."""
        dll_path = os.path.join(REPO_DIR, "SimpleApp.Tests", "bin", "Debug", "SimpleApp.Tests.dll")
        assert os.path.isfile(dll_path), f"SimpleApp.Tests.dll not found at {dll_path}"

    def test_test_dll_is_nonempty(self):
        """SimpleApp.Tests.dll is a non-empty file."""
        dll_path = os.path.join(REPO_DIR, "SimpleApp.Tests", "bin", "Debug", "SimpleApp.Tests.dll")
        assert os.path.isfile(dll_path), f"SimpleApp.Tests.dll not found at {dll_path}"
        size = os.path.getsize(dll_path)
        assert size > 0, f"SimpleApp.Tests.dll is empty (size={size})"

    def test_nunit_framework_dll_present(self):
        """NUnit framework DLL is copied to test output directory."""
        nunit_path = os.path.join(
            REPO_DIR, "SimpleApp.Tests", "bin", "Debug", "nunit.framework.dll"
        )
        assert os.path.isfile(nunit_path), f"nunit.framework.dll not found at {nunit_path}"
