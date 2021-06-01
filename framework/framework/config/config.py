from collections.abc import Mapping
from typing import Iterator

from .providers import Provider

GLOBAL_CONFIG = None


def get_config():
    global GLOBAL_CONFIG

    if not GLOBAL_CONFIG:
        GLOBAL_CONFIG = Config()
    return GLOBAL_CONFIG


class Config(Mapping):
    def __init__(self):
        self.__properties: dict[str, str] = {}

    def update_with(self, provider: Provider):
        self.__properties.update(
            {
                key: value
                for key, value in provider.items()
                if key not in self.__properties
            }
        )

    def __getitem__(self, k: str) -> str:
        return self.__properties[k]

    def __iter__(self) -> Iterator[str]:
        yield from self.__properties

    def __len__(self) -> int:
        return len(self.__properties)

    def __repr__(self) -> str:
        props_repr = ", ".join(
            f"{key}={value}" for key, value in self.__properties.items()
        )
        return f"{self.__class__.__name__}({props_repr})"
