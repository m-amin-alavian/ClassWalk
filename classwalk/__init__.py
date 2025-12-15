from typing import Literal

import pandas as pd

from .handler import open_raw_table, open_cleaned_table


_Form = Literal["Raw", "Cleaned"]


_Classification = Literal[
    "COICOP1999",
    "COICOP1999_IR",
    "COICOP1999_to_CPC1",
    "COICOP2018",
    "COICOP2018_IR",
    "COICOP2018_to_COICOP1999",
    "CPC1",
    "CPC1_to_CPC11",
    "CPC1_to_ISIC3",
    "CPC11",
    "CPC11_to_CPC1",
    "CPC11_to_CPC2",
    "CPC2",
    "CPC2_to_CPC21",
    "CPC21",
    "ISIC3",
    "ISIC3_to_ISIC2",
    "ISIC3_to_ISIC31",
    "ISIC31",
    "ISIC31_to_CPC11",
    "ISIC31_to_ISIC4",
    "ISIC31_IR",
    "ISIC31_IR_to_ISIC4_IR",
    "ISIC4",
    "ISIC4_IR",
    "ISIC4_to_ISIC31",
    "ISIC4_to_ISIC5",
    "ISIC4_to_CPC2",
    "ISIC4_to_CPC21",
    "CPA2008",
    "CPA2008_to_CPA21",
    "CPA2008_to_ECOICOP",
    "CPA21",
    "ECOICOP",
    "ECOICOP_to_ECOICOP2",
    "ECOICOP_to_CPA2008",
    "ECOICOP_to_CPA21",
    "ECOICOP",
    "ECOICOP2_to_ECOICOP",
    "NACE2",
    "NACE2_to_CPA2008",
    "NACE2_to_ISIC4",
]


def open_classification_table(
    name: _Classification,
    form: _Form,
    **kwargs,
) -> pd.DataFrame:
    name = name.lower()
    if form == "Cleaned":
        open_cleaned_table(name, **kwargs)
    elif form == "Raw":
        open_raw_table(name, **kwargs)
