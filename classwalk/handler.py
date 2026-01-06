"""
handler.py

This module provides functions for downloading, reading, and cleaning raw data files
as specified in the project metadata. It supports automatic file retrieval, flexible
reader selection (custom or default), and post-processing such as adding alpha codes.

Functions
---------
- download(name): Download a raw data file by name from a URL in metadata.
- open_raw_table(name): Open a raw data table as a pandas DataFrame, downloading if needed.
- open_cleaned_table(name, add_alpha_code): Open and clean a data table, optionally adding an alpha code column.
- get_files(): Get a mapping of file stems to file paths in the data directory.
- create_alpha_code(column): Generate an 'Alpha_Code' column based on uppercase letters in a pandas Series.

Dependencies
------------
- pandas
- requests
- pathlib
- Project modules: utils.metadata, utils.settings, reader, cleaner
"""
from pathlib import Path

import requests

import pandas as pd

from .utils import metadata, settings
from . import reader, cleaner


SUFFIX_LIST = (".xls", ".xlsx", ".txt", ".csv")

def download(name: str) -> None:
    """
    Download a raw data file by its name from the URL specified in metadata.

    The function retrieves the URL from the metadata, downloads the file,
    determines the correct file suffix, and saves it to the data directory.

    Parameters
    ----------
    name : str
        The key name of the file to download, as specified in metadata.raw_files.

    Raises
    ------
    RuntimeError
        If the HTTP request fails.
    ValueError
        If the file suffix cannot be determined.
    """
    url = metadata.raw_files[name]["url"]
    response = requests.get(
        url,
        headers={
            "user-agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/142.0.0.0 Safari/537.36",
        }
    )
    if response.status_code != 200:
        raise RuntimeError(f"Failed to download {url}: {response.status_code}")


    suffix = "." + url.rsplit(".", 1)[-1].lower()
    if suffix not in SUFFIX_LIST:
        suffix = next((s for s in SUFFIX_LIST if s in url.lower()), None)
    if not suffix:
        raise ValueError(f"Unknown file suffix for {url}")
    file_name = f"{name}{suffix}"
    with settings.data_directory.joinpath(file_name).open(mode="wb") as file:
        file.write(response.content)


def open_raw_table(name: str) -> pd.DataFrame:
    """
    Open a raw data table by name, downloading the file if necessary.

    This function locates the file in the data directory (downloading it if not present),
    determines the appropriate reader function (custom, specified in metadata, or default),
    and loads the file into a pandas DataFrame.

    Parameters
    ----------
    name : str
        The key name of the file to open, as specified in metadata.raw_files.

    Returns
    -------
    pandas.DataFrame
        The loaded raw data table.

    Raises
    ------
    ValueError
        If the file suffix is unsupported.
    RuntimeError
        If the file cannot be downloaded.
    """
    name = name.lower()
    files = get_files()
    if name not in files:
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
        else:
            raise ValueError(f"Unsupported file suffix: {suffix}")
    table = reader_function(file)
    return table


def open_cleaned_table(
    name: str,
    add_alpha_code: bool = False
) -> pd.DataFrame:
    """
    Open and clean a data table by name.

    This function loads the raw data table, applies the corresponding cleaning function,
    and optionally adds an 'Alpha_Code' column.

    Parameters
    ----------
    name : str
        The key name of the file to open and clean, as specified in metadata.raw_files.
    add_alpha_code : bool, optional
        Whether to add an 'Alpha_Code' column based on the 'Code' column (default is False).

    Returns
    -------
    pandas.DataFrame
        The cleaned data table.
    """
    table = (
        open_raw_table(name)
        .pipe(getattr(cleaner, name.lower()))
    )
    if add_alpha_code:
        table["Alpha_Code"] = create_alpha_code(table["Code"])
    return table



def get_files() -> dict[str, Path]:
    """
    Get all files in the data directory as a mapping from file stem to Path.

    Returns
    -------
    dict of str to Path
        Dictionary mapping file stem (name without suffix) to file Path object.
    """
    return {file.stem: file for file in settings.data_directory.iterdir()}


def create_alpha_code(column: pd.Series) -> pd.Series:
    """
    Create an 'Alpha_Code' column based on uppercase letters in the input column.

    For each value, if it contains an uppercase letter, it is used as-is;
    otherwise, the previous non-null value is forward-filled and concatenated
    with the current value (or an empty string).

    Parameters
    ----------
    column : pandas.Series
        The column from which to generate the alpha code.

    Returns
    -------
    pandas.Series
        The generated alpha code series.
    """
    filt = column.str.contains("[A-Z]")
    return column.where(filt, None).ffill() + column.where(-filt, "")
