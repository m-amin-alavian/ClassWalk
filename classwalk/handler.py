from pathlib import Path

import requests

import pandas as pd

from .utils import metadata, settings
from . import reader, cleaner


SUFFIX_LIST = [".xls", ".xlsx", ".txt", ".csv"]

def download(name: str) -> None:
    url = metadata.raw_files[name]["url"]
    response = requests.get(url)
    assert response.status_code == 200

    suffix = "." + url.rsplit(".", 1)[-1]
    if suffix not in SUFFIX_LIST:
        for s in SUFFIX_LIST:
            if s in url:
                suffix = s
    if suffix not in SUFFIX_LIST:
        raise ValueError
    file_name = f"{name}{suffix}"
    with settings.data_directory.joinpath(file_name).open(mode="wb") as file:
        file.write(response.content)


def open_raw_table(name: str) -> pd.DataFrame:
    files = get_files()
    if not name in files:
        download(name)
        files = get_files()

    file = files[name]
    file_metadata = metadata.raw_files[name]
    suffix = file.suffix.lower()

    if hasattr(reader, name):
        reader_function = getattr(reader, name)
    elif "read_function" in file_metadata:
        reader_function = getattr(reader, file_metadata["read_function"])
    else:
        read_options = {"dtype": str}
        read_options.update(file_metadata.get("read_options", {}))
        if suffix in [".xls", ".xlsx"]:
            reader_function = lambda path: pd.read_excel(path, **read_options) # type: ignore
        elif suffix in [".txt", ".csv"]:
            reader_function = lambda path: pd.read_csv(path, **read_options) # type: ignore
    table = reader_function(file)
    return table


def open_cleaned_table(name: str) -> pd.DataFrame:
    return (
        open_raw_table(name)
        .pipe(getattr(cleaner, name))
    )


def get_files() -> dict[str, Path]:
    return {
        file.stem: file for file in settings.data_directory.iterdir()
    }
