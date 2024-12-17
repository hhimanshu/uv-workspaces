from dataclasses import dataclass, field
from pathlib import PurePosixPath


@dataclass
class Endpoint:
    """
    Represents an API endpoint with its path and nested routes.
    Supports hierarchical path structures with dot notation access.
    """

    path: str
    routes: dict[str, "Endpoint"] = field(default_factory=dict)

    def __post_init__(self):
        """Normalize the path after initialization."""
        self.path = str(PurePosixPath(self.path))

    def __getattr__(self, name: str) -> "Endpoint":
        """Enable dot notation access to nested routes."""
        if name in self.routes:
            return self.routes[name]
        raise AttributeError(f"'{self.__class__.__name__}' has no route '{name}'")


class ApiEndpoints:
    """Central registry of API endpoints."""

    ROOT = Endpoint(path="/")
    API = Endpoint(path="/api")
    DOCS = Endpoint(path="/docs")
    OPENAPI = Endpoint(path="/openapi.json")
    DEBUG = Endpoint(path="/debug")
    HELLO = Endpoint(
        path="/hello",
        routes={
            "ROOT": Endpoint(path="/"),
            "NAME": Endpoint(path="/{name}"),
        },
    )
    USERS = Endpoint(
        path="/users",
        routes={
            "ROOT": Endpoint(path="/"),
        },
    )

    @classmethod
    def get_all_endpoints(cls) -> dict[str, Endpoint]:
        """Get all registered endpoints."""
        return {
            name: value
            for name, value in vars(cls).items()
            if isinstance(value, Endpoint) and not name.startswith("_")
        }
