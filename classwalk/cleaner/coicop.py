import pandas as pd

from ..utils import text_utils


def coicop1999_to_cpc1(raw_table: pd.DataFrame) -> pd.DataFrame:
    return (
        raw_table
        .rename(
            columns={
                "COICOP": "COICOP1999_Code",
                "CPC1.0": "CPC1_Code",
            }
        )
        .loc[:, ["COICOP1999_Code", "CPC1_Code", "Detail"]]
    )


def coicop2018(raw_table: pd.DataFrame) -> pd.DataFrame:
    return (
        raw_table
        .rename(columns={"code": "Code", "title": "Description"})
        .assign(Level = lambda df: df["Code"].str.count("\\.").add(1))
        .loc[:, ["Code", "Description", "Level"]]
        .sort_values("Code")
        .reset_index(drop=True)
    )


def coicop2018_ir(raw_table: pd.DataFrame) -> pd.DataFrame:
    return (
        raw_table
        .set_axis(["Code", "Description"], axis="columns")
        .assign(
            Level = lambda df: df["Code"].str.len().sub(1),

            Description=lambda df: text_utils.clean_farsi_text(df["Description"]),
        )
        .drop_duplicates("Code")
        .reset_index(drop=True)
    )
