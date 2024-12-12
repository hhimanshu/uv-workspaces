import subprocess
from .utils import get_workspace_root, ensure_virtualenv


def run_tests(package=None):
    """
    Runs tests for the specified package or all packages.

    Args:
        package (str, optional): Package name to test ('api' or 'app').
                               If None, tests all packages.
    """
    ensure_virtualenv()
    workspace_root = get_workspace_root()

    if package == "api":
        test_path = workspace_root / "packages" / "api" / "tests"
        subprocess.run(["pytest", str(test_path), "-v"])
    elif package == "app":
        test_path = workspace_root / "packages" / "app" / "tests"
        subprocess.run(["pytest", str(test_path), "-v"])
    else:
        print("Running all tests...")
        for pkg in ["api", "app"]:
            test_path = workspace_root / "packages" / pkg / "tests"
            subprocess.run(["pytest", str(test_path), "-v"])


if __name__ == "__main__":
    import sys

    package = sys.argv[1] if len(sys.argv) > 1 else None
    run_tests(package)
