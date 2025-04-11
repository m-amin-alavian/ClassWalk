from ..handler import open_cleaned_table

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
    .assign(Default_Ratio=lambda df: df["ISIC31_Count"].astype("Float64").pow(-1))
)

table.to_excel("isic31_ir_to_isic4_ir.xlsx", index=False)
