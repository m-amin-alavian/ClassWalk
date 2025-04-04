import pandas as pd


def isic3(raw_table: pd.DataFrame) -> pd.DataFrame:
    return (
        raw_table
        .assign(Level = lambda df: df["Code"].str.len())
    )


def isic31(raw_table: pd.DataFrame) -> pd.DataFrame:
    return (
        raw_table
        .assign(Level = lambda df: df["Code"].str.len())
    )


def isic31_ir(raw_table: pd.DataFrame) -> pd.DataFrame:
    return (
        raw_table
        .set_axis(["Code", "Description"], axis="columns")
        .assign(
            Code=lambda df: df["Code"].str.strip(),
            Level=lambda df: df["Code"].str.len()
            .where(df["Code"].str.contains("[A-Z0-9]"), 1),
        )
        .drop_duplicates("Code", keep="first")
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
        .assign(
            Code=lambda df: df["Code"].str.strip(),
            Level=lambda df: df["Code"].str.len()
            .where(df["Code"].str.contains("[A-Z0-9]"), 1),
        )
        .drop_duplicates("Code", keep="first")
    )
