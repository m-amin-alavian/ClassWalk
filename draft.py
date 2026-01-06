import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    from classwalk import open_cleaned_table, open_raw_table, open_classification_table
    return open_classification_table, open_cleaned_table, open_raw_table


@app.cell
def _(open_classification_table):
    open_classification_table("isco88_to_isco08_ir", "Cleaned")
    return


@app.cell
def _(open_cleaned_table):
    open_cleaned_table("ISCO88_IR")
    return


@app.cell
def _(open_cleaned_table):
    isco_table = (
        open_cleaned_table("ISCO88")
        .rename(columns={"Description": "Title"})
        .rename(columns=lambda n: n.lower())
        .assign(title=lambda df: df["title"].str.strip())
        .assign(
            label=lambda df:
            df["title"]
            .str.lower()
            .str.replace(" ", "_")
            .str.replace("-", "_")
            .str.replace("'", "")
            .str.replace(",", "")
            .str.replace(")", "")
            .str.replace("(", "")
            .str.replace("_+", "_", regex=True)
        )
        .merge(
            open_cleaned_table("ISCO88_IR")
            .rename(columns={"Description": "Farsi_Title", "Level": "Farsi_Level"})
            .assign(
                Farsi_Title=lambda df:
                df["Farsi_Title"].str.replace("‎", "‌").str.replace("ي", "ی").str.replace("ك", "ک").str.strip()
            )
            .assign(Farsi_Level=lambda df: df["Farsi_Level"].astype(int).astype(str))
            .rename(columns=lambda n: n.lower()),
            on="code",
            how="outer",
        )
        .sort_values("code")
        .assign(level=lambda df: df["level"].fillna(df["farsi_level"]))
    )
    return (isco_table,)


@app.cell
def _(isco_table):
    isco_table
    return


@app.cell
def _(isco_table):
    with open("isco_88.yaml", mode="w", encoding="utf-8") as file:
        for _, row in isco_table.iterrows():
            if row["level"] >= "4":
                code = row["code"]
            else:
                end = f"{row["code"][:-1]}{int(row["code"][-1])+1}"

                start_str = f"{row["code"]:0<4}"
                end_str = f"{end:0<4}"
                code = f"{{start: {int(start_str)}, end: {int(end_str)}}}"
            if isinstance(row["farsi_title"], str):
                comment = ""
            else:
                comment = "# "
            print(
        f"""
        {comment}'{row["code"]}':
        {comment}  level: {row["level"]}
        {comment}  label: {row["label"]}
        {comment}  title: {row["title"]}
        {comment}  farsi_title: {row["farsi_title"]}
        {comment}  code: {code}""",
        file=file,
        )
    return


@app.cell
def _(open_raw_table):
    open_raw_table("COICOP2018")["code"].str.count("\\.").add(1)
    return


@app.cell
def _(open_cleaned_table):
    open_cleaned_table("coicop2018")
    return


if __name__ == "__main__":
    app.run()
