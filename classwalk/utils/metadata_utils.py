from pathlib import Path
from typing import NamedTuple

import yaml


SETTINGS_PATH = Path("classwalk_settings.yaml")
PACKAGE_PATH = Path(__file__).parents[1]


def read_yaml_file(path: Path) -> dict:
    with path.open() as file:
        return yaml.safe_load(file)


def read_metadata(name: str) -> dict:
    return read_yaml_file(PACKAGE_PATH.joinpath("metadata", f"{name}.yaml"))


class Settings(NamedTuple):
    data_directory: Path = Path("Data")


class Metadata(NamedTuple):
    raw_files: dict[str, dict] = read_metadata("raw_files")


setting_dict = read_yaml_file(SETTINGS_PATH) if SETTINGS_PATH.exists() else {}
settings = Settings(**setting_dict)
settings.data_directory.mkdir(exist_ok=True, parents=True)

metadata = Metadata()
