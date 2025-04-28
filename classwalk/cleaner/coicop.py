import pandas as pd


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
