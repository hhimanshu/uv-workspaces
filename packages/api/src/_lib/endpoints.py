from dataclasses import dataclass, field
from typing import Any


@dataclass
class Api:
    path: str
    routes: dict[str, "Api"] = field(default_factory=dict)
    params: list[str] = field(default_factory=list)
    query_params: list[str] = field(default_factory=list)

    def __getattr__(self, name):
        if name in self.routes:
            return self.routes[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")


class Endpoints:
    ROOT = Api(path="/")
    API = Api(path="/api")
    DOCS = Api(path="/docs")
    OPENAPI = Api(path="/openapi.json")
    DEBUG = Api(path="/debug")
    # HELLO = Api(
    #     path="/hello",
    #     routes={
    #         "GREET": Api(path="/greet/{name}", params=["name"]),
    #         "TODAY": Api(path="/today", query_params=["format"]),
    #     },
    # )
    # MATH = Api(path="/math")
    # DISHES = Api(
    #     path="/dishes",
    #     routes={
    #         "SEARCH": Api(path="/search"),
    #     },
    # )
    # CLEANCARROT = Api(
    #     path="/cleancarrot",
    #     routes={
    #         "SEARCH_SESSIONS": Api(path="/search-sessions"),
    #         "SEARCH_SESSION": Api(
    #             path="/search-sessions/{search_session_id}",
    #             params=["search_session_id"],
    #         ),
    #         "FEEDBACKS": Api(
    #             path="/search-sessions/{search_session_id}/feedbacks",
    #             params=["search_session_id"],
    #         ),
    #     },
    # )

    @classmethod
    def get_full_path(cls, *args: Any, **kwargs: Any) -> str:
        """
        Get the full path by combining multiple ApiInfo objects or strings,
        with optional parameter and query parameter substitutions.
        """
        path_parts = []
        query_params = {}

        for arg in args:
            if isinstance(arg, Api):
                path_part = arg.path
                for param in arg.params:
                    if param in kwargs:
                        path_part = path_part.replace(f"{{{param}}}", str(kwargs[param]))
                path_parts.append(path_part.strip("/"))

                for q_param in arg.query_params:
                    if q_param in kwargs:
                        query_params[q_param] = kwargs[q_param]
            elif isinstance(arg, str):
                path_parts.append(arg.strip("/"))
            else:
                raise ValueError(f"Unsupported type: {type(arg)}")

        full_path = "/" + "/".join(path_parts)

        if query_params:
            query_string = "&".join(f"{k}={v}" for k, v in query_params.items())
            full_path += f"?{query_string}"

        return full_path
