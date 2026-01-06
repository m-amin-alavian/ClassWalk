import lfsir

(
    lfsir.load_table(years="1384-95")
    .dropna(subset="Main_Job_Title_ISCO_Code")
    .loc[lambda df: df["Main_Job_Title_ISCO_Code"].gt(0)]
    .assign(Code=lambda df: df["Main_Job_Title_ISCO_Code"].astype(str).str.pad(4, "left", "0"))
    .groupby(["Code", "Year"])["Weight"].sum()
    .unstack(fill_value=0)
    .pipe(lambda df: df.div(df.sum(), axis="columns"))
    .to_csv("isco88_employment_share_lfs.csv", float_format="%.6f")
)

(
    lfsir.load_table(years="1396-1401")
    .dropna(subset="Main_Job_Title_ISCO_Code")
    .loc[lambda df: df["Main_Job_Title_ISCO_Code"].gt(0)]
    .assign(Code=lambda df: df["Main_Job_Title_ISCO_Code"].astype(str).str.pad(4, "left", "0"))
    .groupby(["Code", "Year"])["Weight"].sum()
    .unstack(fill_value=0)
    .pipe(lambda df: df.div(df.sum(), axis="columns"))
    .to_csv("isco08_employment_share_lfs.csv", float_format="%.6f")
)
