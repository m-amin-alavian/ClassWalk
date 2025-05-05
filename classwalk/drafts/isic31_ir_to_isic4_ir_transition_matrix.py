import pandas as pd

from classwalk.handler import open_cleaned_table
from classwalk.drafts.transition_matrix_weight_calculation import isic31_to_isic4_calculate_transition_weights


def main() -> pd.DataFrame:
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
        .join(
            isic31_to_isic4_calculate_transition_weights(1, 1).rename("Weight_1y_1c"),
            on=["ISIC31_Code", "ISIC4_Code"],
        )
        .join(
            isic31_to_isic4_calculate_transition_weights(2, 1).rename("Weight_2y_1c"),
            on=["ISIC31_Code", "ISIC4_Code"],
        )
        .join(
            isic31_to_isic4_calculate_transition_weights(3, 1).rename("Weight_3y_1c"),
            on=["ISIC31_Code", "ISIC4_Code"],
        )
        .join(
            isic31_to_isic4_calculate_transition_weights(1, 5).rename("Weight_1y_5c"),
            on=["ISIC31_Code", "ISIC4_Code"],
        )
        .join(
            isic31_to_isic4_calculate_transition_weights(2, 5).rename("Weight_2y_5c"),
            on=["ISIC31_Code", "ISIC4_Code"],
        )
        .join(
            isic31_to_isic4_calculate_transition_weights(3, 5).rename("Weight_3y_5c"),
            on=["ISIC31_Code", "ISIC4_Code"],
        )
    )
    for col in [
        "Weight_1y_1c",
        "Weight_2y_1c",
        "Weight_3y_1c",
        "Weight_1y_5c",
        "Weight_2y_5c",
        "Weight_3y_5c",
    ]:
        table[col] = table[col].fillna(0).where(table["ISIC31_Code"].notna(), None)

    return table


if __name__ == "__main__":
    result = main()
    result.to_excel("ISIC31_to_ISIC4_Transition_Weights.xlsx", index=False)
    (
        result
        .drop(
            columns=[
                "Description",
                "ISIC31_Description",
                "ISIC4_Description",
            ]
        )
        .dropna(how="all")
        .to_csv("ISIC31_to_ISIC4_Transition_Weights.csv", index=False)
    )
