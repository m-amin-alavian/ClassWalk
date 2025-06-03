from pathlib import Path
import re

import pandas as pd


def read_file(path: Path) -> str:
    """
    Read the entire contents of a file and return it as a string.

    Parameters
    ----------
    path : Path
        The path to the file to be read.

    Returns
    -------
    str
        The contents of the file as a string.
    """
    with path.open(encoding="utf-8") as file:
        return file.read()


def get_tsv_data(path: Path) -> list[list[str]]:
    """
    Parse a TSV-like file where columns are separated by 3 or more spaces.

    Parameters
    ----------
    path : Path
        The path to the TSV-like file.

    Returns
    -------
    list of list of str
        The parsed data as a list of rows, each row being a list of strings.
    """
    return [
        re.split("\\s{3,}", row) for row in
        read_file(path).split("\n")[:-1]
    ]


def read_tsv(path: Path) -> pd.DataFrame:
    """
    Read a TSV-like file and return it as a pandas DataFrame.

    The first row is used as column headers.

    Parameters
    ----------
    path : Path
        The path to the TSV-like file.

    Returns
    -------
    pandas.DataFrame
        The data as a DataFrame with appropriate column headers.
    """
    data = get_tsv_data(path)
    table = pd.DataFrame(data=data[1:], columns=data[0])
    return table


def coicop1999(path: Path) -> pd.DataFrame:
    """
    Read a COICOP 1999 formatted TSV-like file and return it as a pandas DataFrame.

    The first row is used as column headers.

    Parameters
    ----------
    path : Path
        The path to the COICOP 1999 file.

    Returns
    -------
    pandas.DataFrame
        The data as a DataFrame with appropriate column headers.
    """
    table = pd.DataFrame(get_tsv_data(path))
    table.columns = table.iloc[0]
    table = table.iloc[1:]

    return table

