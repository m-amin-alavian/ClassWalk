import pandas as pd

from .utils import text_utils


def isic3(raw_table: pd.DataFrame) -> pd.DataFrame:
    return (
        raw_table
        .assign(Level = lambda df: df["Code"].str.len())
    )


def isic31(raw_table: pd.DataFrame) -> pd.DataFrame:
    return (
        raw_table
        .assign(
            Level = lambda df: df["Code"].str.len()
        )
    )


def isic31_ir(raw_table: pd.DataFrame) -> pd.DataFrame:
    return (
        raw_table
        .set_axis(["Code", "Description"], axis="columns")
        .assign(
            Code=lambda df: df["Code"].str.strip(),

            Level=lambda df: df["Code"].str.len()
            .where(df["Code"].str.contains("[A-Z0-9]"), 1),

            Description=lambda df: text_utils.clean_farsi_text(df["Description"]),
        )
        .assign(
            Code=lambda df: text_utils.map_farsi_alphabet(df["Code"])
        )
        .drop_duplicates("Code", keep="first")
        .loc[lambda df: - df["Code"].str.startswith("X")]
        .pipe(_add_missing_level4_items)
    )


def isic31_to_isic4(raw_table: pd.DataFrame) -> pd.DataFrame:
    return (
        raw_table
        .rename(columns={"ISIC31code": "ISIC31_Code", "ISIC4code": "ISIC4_Code"})
        .loc[:, ["ISIC31_Code", "ISIC4_Code"]]
    )


def isic4(raw_table: pd.DataFrame) -> pd.DataFrame:
    return (
        raw_table
        .assign(Level = lambda df: df["Code"].str.len())
    )


def isic4_ir(raw_table: pd.DataFrame) -> pd.DataFrame:
    return (
        raw_table
        .set_axis(["Code", "Description"], axis="columns")

        .loc[lambda df: df["Code"].ne("53950")]

        .assign(
            Code=lambda df: df["Code"].str.strip(),

            Level=lambda df: df["Code"].str.len()
            .where(df["Code"].str.contains("[A-Z0-9]"), 1),

            Description=lambda df: text_utils.clean_farsi_text(df["Description"]),
        )
        .assign(
            Code=lambda df: text_utils.map_farsi_alphabet(df["Code"])
        )
        .drop_duplicates("Code", keep="first")
        .loc[lambda df: - df["Code"].str.startswith("X")]
        .pipe(_add_missing_level4_items)
    )


def _add_missing_level4_items(table: pd.DataFrame) -> pd.DataFrame:
    missing_level4_codes = (
        table.loc[lambda df: df["Level"].eq(5)]["Code"]
        .str.slice(0, -1)
        .loc[lambda s: - s.isin(table["Code"])]
    )
    missing_level4_items = (
        table.loc[lambda df: df["Code"].isin(missing_level4_codes + "0")]
        .assign(
            Code = lambda df: df["Code"].str.slice(0, -1),
            Level = lambda df: df["Level"].sub(1),
        )
    )
    missing_level4_items.index = missing_level4_items.index - 0.5
    table = pd.concat(
        [
            table,
            missing_level4_items,
        ],
    )
    table = table.sort_index()
    return table
