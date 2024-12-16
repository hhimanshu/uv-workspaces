import os
import subprocess
import sys
from pathlib import Path


def ensure_pre_commit_installed():
    """
    Ensures pre-commit is installed in our virtual environment.
    We install it using uv to maintain consistency with our package management.
    """
    print("Ensuring pre-commit is installed...")
    subprocess.run(["uv", "pip", "install", "pre-commit"], check=True)


def install_pre_commit_hooks():
    """
    Configures pre-commit hooks for our repository.
    This step runs after we ensure pre-commit is installed.
    """
    print("Setting up pre-commit hooks...")
    subprocess.run(["pre-commit", "install"], check=True)
    print("Running pre-commit on all files for initial setup...")
    subprocess.run(["pre-commit", "run", "--all-files"], check=True)


def install_workspace():
    """
    Installs all workspace packages in development mode.
    Each package is installed separately to handle dependencies properly.
    """
    print("\nInstalling workspace packages...")
    workspace_root = Path(__file__).parent.parent
    api_dir = workspace_root / "packages" / "api"
    app_dir = workspace_root / "packages" / "app"

    if api_dir.exists():
        print(f"\nInstalling {api_dir.name} package...")
        subprocess.run(["uv", "pip", "install", "-e", f"{api_dir}[dev]"], check=True)

    if app_dir.exists():
        print(f"\nInstalling {app_dir.name} package...")
        subprocess.run(["uv", "pip", "install", "-e", f"{app_dir}[dev]"], check=True)


def verify_environment():
    """
    Checks that we're running in a proper development environment.
    This verifies the virtual environment is activated before proceeding.
    """
    if "VIRTUAL_ENV" not in os.environ:
        print("Error: Virtual environment not activated.")
        print("Please activate your virtual environment first:")
        print("source .venv/bin/activate")
        sys.exit(1)


def main():
    """
    Orchestrates the complete development environment setup.
    This runs all setup steps in the correct order, with proper error handling.
    """
    try:
        print("Starting development environment setup...\n")
        verify_environment()

        # First, install pre-commit itself
        ensure_pre_commit_installed()

        # Then set up the hooks
        install_pre_commit_hooks()

        # Finally, install workspace packages
        install_workspace()

        print("\n✨ Setup complete! Your development environment is ready.")
        print("\nYou can now:")
        print("  - Run the server: python -m scripts.dev")
        print("  - Run tests: python -m scripts.test")
        print("  - Git commits will automatically run pre-commit checks")

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error during setup: {e}")
        print("Please check the error message above and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
