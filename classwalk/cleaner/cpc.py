import pandas as pd


def cpc1_to_cpc11(raw_table: pd.DataFrame) -> pd.DataFrame:
    return (
        raw_table
        .rename(
            columns={
                "CPCv10code": "CPC1_Code",
                "CPCv11code": "CPC11_Code",
            }
        )
        .loc[:, ["CPC1_Code", "CPC11_Code", "Detail"]]
    )


def cpc11_to_cpc2(raw_table: pd.DataFrame) -> pd.DataFrame:
    return (
        raw_table
        .rename(
            columns={
                "CPC11Code": "CPC11_Code",
                "CPC2Code": "CPC2_Code",
            }
        )
        .loc[:, ["CPC11_Code", "CPC2_Code"]]
    )
