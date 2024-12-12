import os
import subprocess
import sys
from pathlib import Path
import asyncio
import motor.motor_asyncio


class WorkspaceManager:
    """
    Manages workspace-specific operations and configurations.
    This class handles workspace initialization, database connections,
    and service startup for different workspaces.
    """

    def __init__(self):
        self.workspace_root = Path(__file__).parent.parent
        self.services = {}
        self.db_clients = {}

    def get_workspace_path(self, workspace: str) -> Path:
        """Returns the path for a specific workspace"""
        return self.workspace_root / "packages" / workspace

    async def init_db_connection(self, workspace: str) -> None:
        """
        Initializes database connection for a workspace.
        Each workspace gets its own database in MongoDB.
        """
        # MongoDB connection string from environment or default to local
        mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)

        # Each workspace gets its own database
        db = client[f"{workspace}_db"]

        # Store the client for cleanup
        self.db_clients[workspace] = client

        # Basic connectivity test
        try:
            await db.command("ping")
            print(f"Successfully connected to {workspace} database")
        except Exception as e:
            print(f"Database connection failed for {workspace}: {e}")
            raise

    def ensure_docker_running(self) -> None:
        """
        Ensures MongoDB Docker container is running.
        Creates or starts the container if needed.
        """
        try:
            # Check if container exists and is running
            result = subprocess.run(
                ["docker", "ps", "-q", "-f", "name=mongodb"],
                capture_output=True,
                text=True,
            )

            if not result.stdout.strip():
                # Container isn't running, try to start it or create it
                print("Starting MongoDB container...")
                subprocess.run(
                    [
                        "docker",
                        "run",
                        "-d",
                        "--name",
                        "mongodb",
                        "-p",
                        "27017:27017",
                        "-v",
                        "mongodb_data:/data/db",
                        "mongo:latest",
                    ],
                    check=True,
                )
                print("MongoDB container started successfully")
        except subprocess.CalledProcessError as e:
            print(f"Error managing Docker container: {e}")
            raise

    async def init_workspace(self, workspace: str) -> None:
        """Initializes the database for a workspace without starting the app"""
        await self.init_db_connection(workspace)
        print(f"{workspace} workspace database initialized")

    async def start_app(self) -> None:
        """
        Starts the app workspace. Database should be initialized separately.
        This allows the app to connect to the database when needed.
        """
        # App startup logic here - no database initialization
        print("App workspace started")

    def start_api(self) -> None:
        """Starts the FastAPI server"""
        api_dir = self.get_workspace_path("api")
        src_dir = api_dir / "src"

        env = os.environ.copy()
        python_path = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = f"{src_dir}{os.pathsep}{python_path}"

        subprocess.Popen(
            [
                "uvicorn",
                "main:app",
                "--reload",
                "--reload-dir",
                str(src_dir),
                "--host",
                "0.0.0.0",
                "--port",
                os.getenv("PORT", "8000"),
            ],
            env=env,
            cwd=api_dir,
        )


async def main():
    """
    Main entry point that provides different startup combinations
    """
    if len(sys.argv) < 2:
        print("Usage: python dev.py [app|api|all]")
        sys.exit(1)

    command = sys.argv[1]
    manager = WorkspaceManager()

    try:
        if command == "init":
            # Initialize database for specified workspace
            if len(sys.argv) < 3:
                print("Usage: python dev.py init [workspace_name]")
                sys.exit(1)
            workspace = sys.argv[2]
            manager.ensure_docker_running()
            await manager.init_workspace(workspace)
            # Exit after initialization
            sys.exit(0)

        # For other commands, ensure MongoDB is running
        manager.ensure_docker_running()

        if command == "app":
            await manager.start_app()
        elif command == "api":
            await manager.start_app()  # We still need app for API
            manager.start_api()
        elif command == "all":
            await manager.start_app()
            manager.start_api()
            # Add more services as needed
        else:
            print(f"Unknown command: {command}")
            sys.exit(1)

        # Keep the main process running
        while True:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    except Exception as e:
        print(f"\nError during startup: {e}")
        print("\nTroubleshooting steps:")
        print("1. Ensure Docker is running")
        print("2. Check if MongoDB container is accessible")
        print("3. Verify workspace paths are correct")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
