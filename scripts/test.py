import subprocess
from pathlib import Path
from .utils import get_workspace_root, ensure_virtualenv


def run_tests(package=None):
    """
    Runs tests for the specified package or all packages.
    Uses pytest's built-in test discovery to find tests anywhere in the package.
    """
    ensure_virtualenv()
    workspace_root = get_workspace_root()

    # Common pytest arguments for consistent test execution
    pytest_args = [
        "-v",  # Verbose output
        "--tb=short",  # Shorter traceback format
        "--strict-markers",  # Ensure all markers are registered
        "-ra",  # Show extra test summary info
    ]

    def run_package_tests(pkg_path: Path):
        """Run tests for a specific package directory"""
        print(f"\nRunning tests for [{pkg_path.name}] ...")

        # We use pytest's default test discovery - it will automatically find
        # test_*.py and *_test.py files
        subprocess.run(["pytest", str(pkg_path), *pytest_args], cwd=str(pkg_path))

    packages_dir = workspace_root / "packages"
    if package:
        # Run tests for specific package
        pkg_path = packages_dir / package
        if not pkg_path.exists():
            raise ValueError(f"Package '{package}' not found")
        run_package_tests(pkg_path)
    else:
        # Run tests for all packages
        print("Running all tests...")
        for pkg_path in packages_dir.iterdir():
            if pkg_path.is_dir() and not pkg_path.name.startswith("."):
                run_package_tests(pkg_path)


if __name__ == "__main__":
    import sys
    from textwrap import dedent

    # Add help text
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help"]:
        print(
            dedent("""
            Test Runner

            Usage: python -m scripts.test [package_name]

            Arguments:
                package_name    Optional. Name of package to test ('api' or 'app').
                              If omitted, tests all packages.

            Examples:
                python -m scripts.test         # Test all packages
                python -m scripts.test app     # Test only app package
                python -m scripts.test api     # Test only api package
        """)
        )
        sys.exit(0)

    package = sys.argv[1] if len(sys.argv) > 1 else None
    run_tests(package)
