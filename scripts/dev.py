import os
import subprocess
import sys
from pathlib import Path


def start_server():
    """
    Starts the FastAPI development server with proper Python path configuration.

    We need to ensure Python can find our package modules by:
    1. Changing to the api package directory
    2. Setting up the Python path to include our source directory
    3. Starting uvicorn with the correct module path
    """
    # Get the workspace and package directories
    workspace_root = Path(__file__).parent.parent
    api_dir = workspace_root / "packages" / "api"
    src_dir = api_dir / "src"

    # Change to the api directory
    os.chdir(api_dir)

    # Set up the Python path to include our source directory
    env = os.environ.copy()
    python_path = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = f"{src_dir}{os.pathsep}{python_path}"

    print("Starting API server...")
    print(f"API directory: {api_dir}")
    print(f"Source directory: {src_dir}")
    print(f"PYTHONPATH: {env['PYTHONPATH']}")

    # Start the server with the correct module path
    subprocess.run(
        [
            "uvicorn",
            "main:app",  # Changed from "api.main:app"
            "--reload",
            "--reload-dir",
            str(src_dir),
            "--host",
            "0.0.0.0",
            "--port",
            os.getenv("PORT", "8000"),
        ],
        env=env,
    )


def main():
    """Entry point for the development server script"""
    try:
        start_server()
    except Exception as e:
        print(f"\nError starting server: {e}")
        print("\nTroubleshooting steps:")
        print("1. Make sure you've run 'python -m scripts.setup' first")
        print("2. Check that all required files exist in packages/api/src")
        print("3. Verify your virtual environment is activated")
        sys.exit(1)


if __name__ == "__main__":
    main()
