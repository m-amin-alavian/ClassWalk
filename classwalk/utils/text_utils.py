import pandas as pd


FA_TO_EN_ALPHABET = {
    "الف": "A",
    "ب": "B",
    "پ": "C",
    "ت": "D",
    "ث": "E",
    "ج": "F",
    "چ": "G",
    "ح": "H",
    "خ": "I",
    "د": "J",
    "ذ": "K",
    "ر": "L",
    "ز": "M",
    "ژ": "N",
    "س": "O",
    "ش": "P",
    "ص": "Q",
    "ض": "R",
    "ط": "S",
    "ظ": "T",
    "ع": "U",
}

INVISIBLE_CHARS = [
    chr(173),
    chr(8203),
    chr(8206),
    chr(8207),
    chr(8236),
    chr(8234),
    chr(65279)
]


def clean_farsi_text(column: pd.Series) -> pd.Series:
    for to_replace in [
        (chr(1610), chr(1740)), # ي -> ی
        (chr(1574), chr(1740)), # ئ -> ی
        (chr(1609), chr(1740)), # ى -> ی
        (chr(1571), chr(1575)), # أ -> ا
        (chr(1573), chr(1575)), # إ -> ا
        (chr(1572), chr(1608)), # ؤ -> و
        (chr(1603), chr(1705)), # ك -> ک
        (chr(1728), chr(1607)), # ۀ -> ه
        (chr(1577), chr(1607)), # ة -> ه
    ]:
        column = column.str.replace(*to_replace)
    for character in INVISIBLE_CHARS:
        column = column.str.replace(character, chr(8204))
    return column


def map_farsi_alphabet(column: pd.Series) -> pd.Series:
    return column.replace(FA_TO_EN_ALPHABET)
