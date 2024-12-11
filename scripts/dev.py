import os
import subprocess
import sys
from pathlib import Path


class WorkspaceManager:
    def __init__(self):
        self.workspace_root = Path(__file__).parent.parent
        self.api_dir = self.workspace_root / "packages" / "api"
        self.app_dir = self.workspace_root / "packages" / "app"

    def ensure_virtualenv(self):
        """Ensure we're running in a virtualenv"""
        if not os.environ.get("VIRTUAL_ENV"):
            print("Please activate a virtual environment first")
            sys.exit(1)

    def install_workspace(self):
        """Install all workspace packages in development mode"""
        print("Installing workspace packages...")
        subprocess.run(
            [
                "uv",
                "pip",
                "install",
                "--require-virtualenv",
                "-e",
                f"{self.api_dir}[dev]",
                "-e",
                f"{self.app_dir}[dev]",
            ],
            check=True,
        )

    def start_api(self):
        """Start the API development server"""
        self.ensure_virtualenv()
        print("Starting API server...")
        os.chdir(self.api_dir)  # Change to the api directory
        subprocess.run(
            [
                "uvicorn",
                "src.main:app",  # Update the import path to include the src directory
                "--reload",
                "--reload-dir",
                "src",
                "--host",
                "0.0.0.0",
                "--port",
                os.getenv("PORT", "8000"),
            ]
        )

    def test(self, package=None):
        """Run tests for specified package or all packages"""
        self.ensure_virtualenv()
        if package == "api":
            os.chdir(self.api_dir)
            subprocess.run(["pytest", "tests", "-v"])
        elif package == "app":
            os.chdir(self.app_dir)
            subprocess.run(["pytest", "tests", "-v"])
        else:
            print("Running all tests...")
            subprocess.run(["pytest", str(self.api_dir / "tests"), "-v"])
            subprocess.run(["pytest", str(self.app_dir / "tests"), "-v"])


def main():
    manager = WorkspaceManager()
    commands = {
        "install": manager.install_workspace,
        "start-api": manager.start_api,
        "test": lambda: manager.test(),
        "test-api": lambda: manager.test("api"),
        "test-app": lambda: manager.test("app"),
    }

    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        print(f"Available commands: {', '.join(commands.keys())}")
        sys.exit(1)

    commands[sys.argv[1]]()


if __name__ == "__main__":
    main()
