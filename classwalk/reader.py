from pathlib import Path
import re

import pandas as pd


def read_file(path: Path) -> str:
    with path.open() as file:
        return file.read()


def get_tsv_data(path: Path) -> list[list[str]]:
    return [
        re.split("\\s{3,}", row) for row in
        read_file(path).split("\n")[:-1]
    ]


def read_tsv(path: Path) -> pd.DataFrame:
    data = get_tsv_data(path)
    table = pd.DataFrame(data=data[1:], columns=data[0])
    return table


def coicop1999(path: Path) -> pd.DataFrame:
    table = pd.DataFrame(get_tsv_data(path))
    table.columns = table.iloc[0]
    table = table.iloc[1:]

    return table

