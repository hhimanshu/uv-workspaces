from src._lib.endpoints import ApiEndpoints


def get_api_path(path: str) -> str:
    """Helper function to prepend the API base path."""
    return f"{ApiEndpoints.API.path}{path}"
