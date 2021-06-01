import os
import yaml

from dotenv import load_dotenv
from pathlib import Path

from collections import UserDict

Provider = UserDict


class EnvProvider(Provider):
    def __init__(self):
        super().__init__()

        load_dotenv()

        self.data |= {
            key.removeprefix("TEST_").lower(): value
            for key, value in os.environ.items()
            if key.startswith("TEST_")
        }


class YamlProvider(Provider):
    def __init__(self, source: os.PathLike):
        super().__init__()

        file_vars = yaml.load(Path(source).read_text(encoding="utf-8"))
        if type(file_vars) is not dict:
            raise RuntimeError(f"{source} should only contain key:value pairs")

        self.data |= file_vars


class CustomVarsProvider(Provider):
    pass
