import pandas as pd

from classwalk.handler import open_cleaned_table


def calculate_transition_weights() -> pd.DataFrame:
    table = open_cleaned_table("isic31_ir_to_isic4_ir")
    transition_matrix = (
        table
        .dropna(thresh=2)
        .assign(value=1)
        .set_index(["ISIC31_Code", "ISIC4_Code"])
        .loc[:, "value"]
        .unstack(-1, 0)
    )

    isic31_weight = (
        pd.read_csv(
            "classwalk/internal_data/isic31_employment_share_lfs.csv",
            low_memory=False,
            dtype={"Code": str}
        )
        .set_index("Code")
        .reindex(index=transition_matrix.index)
        .fillna(0)
        .assign(Weight=lambda df: df[["1389", "1390", "1391"]].mean(axis="columns"))
        .assign(
            Weight=lambda df:
            df["Weight"]
            .div(df["Weight"].sum()).mul(99)
            .add(df["Weight"].div(len(df.index)).div(100).mul(1).sum())
        )
        .loc[:, "Weight"]
    )


    isic4_weight = (
        pd.read_csv(
            "classwalk/internal_data/isic4_employment_share_lfs.csv",
            low_memory=False,
            dtype={"Code": str}
        )
        .set_index("Code")
        .reindex(index=transition_matrix.columns)
        .fillna(0)
        .assign(Weight=lambda df: df[["1392", "1393", "1394"]].mean(axis="columns"))
        .assign(
            Weight=lambda df:
            df["Weight"]
            .div(df["Weight"].sum()).mul(99)
            .add(df["Weight"].div(len(df.index)).div(100).mul(1).sum())
        )
        .loc[:, "Weight"]
    )


    transition_matrix_iterations: list[pd.DataFrame] = [
        transition_matrix
        .div(transition_matrix.sum(axis="columns"), axis="index")
        .mul(100)
    ]

    residual = 1
    while residual > 0.001:
        last_tm = transition_matrix_iterations[-1]
        new_tm = (
            last_tm
            .mul(isic31_weight.div(last_tm.sum("columns")), axis="index")
            .mul(isic4_weight.div(last_tm.sum("index")), axis="columns")
        )
        new_tm = new_tm.div(new_tm.sum(axis="columns"), axis="index").mul(100)
        transition_matrix_iterations.append(new_tm)
        residual = new_tm.sub(last_tm).abs().sum().sum()
        print(residual, end="\r")

    transition_weights = (
        transition_matrix_iterations[-1]
        .stack()
        .round(2)
        .loc[lambda s: s.gt(0)]
        .to_frame("Weight") # type: ignore
    )

    return transition_weights
