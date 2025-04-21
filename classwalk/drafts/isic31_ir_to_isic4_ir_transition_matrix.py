import pandas as pd

from classwalk.handler import open_cleaned_table
from classwalk.drafts.transition_matrix_weight_calculation import calculate_transition_weights


def main() ->pd.DataFrame:
    table = (
        open_cleaned_table("isic31_ir_to_isic4_ir")
        .join(
            open_cleaned_table("isic31_ir")
            .set_index("Code")
            .loc[:, "Description"]
            .rename("ISIC31_Description"),
            on="ISIC31_Code"
        )
        .join(
            open_cleaned_table("isic4_ir")
            .set_index("Code")
            .loc[:, "Description"]
            .rename("ISIC4_Description"),
            on="ISIC4_Code"
        )
        .loc[:, ["Description", "ISIC31_Code", "ISIC31_Description", "ISIC4_Code", "ISIC4_Description"]]
    )
    table = (
        table
        .join(
            table["ISIC31_Code"].value_counts().astype("Int16").rename("ISIC31_Count"),
            on="ISIC31_Code"
        )
        .join(
            table["ISIC4_Code"].value_counts().astype("Int16").rename("ISIC4_Count"),
            on="ISIC4_Code"
        )
        .assign(
            Even_Weight=lambda df: df["ISIC31_Count"].astype("Float64").pow(-1).mul(100).round(2)
        )
        .join(calculate_transition_weights(), on=["ISIC31_Code", "ISIC4_Code"])
        .assign(
            Weight=lambda df:
            df["Weight"].fillna(0).where(df["ISIC31_Code"].notna(), None)
        )
    )

    return table


if __name__ == "__main__":
    main().to_excel("ISIC31_to_ISIC4_Transition_Weights.xlsx", index=False)
