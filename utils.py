import pandas as pd
import numpy as np

REQUIRED_COLUMNS = [
    "Date",
    "Investment",
    "Category",
    "Amount",
    "Return",
    "Status",
]


def load_data(uploaded_file):
    """
    Safely load and validate investment data.
    """

    if uploaded_file is None:
        raise ValueError("No CSV file uploaded.")

    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        raise ValueError(f"Unable to read CSV: {e}")

    if df.empty:
        raise ValueError("Uploaded CSV is empty.")

    df.columns = df.columns.str.strip()

    missing = [
        col
        for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing)
        )

    df = df.copy()

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce",
    )

    for col in ["Amount", "Return"]:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce",
        )

    for col in [
        "Investment",
        "Category",
        "Status",
    ]:

        df[col] = (
            df[col]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )

    df = df.dropna(
        subset=[
            "Date",
            "Amount",
            "Return",
        ]
    )

    df["Amount"] = df["Amount"].clip(lower=0)

    df = df.reset_index(drop=True)

    return df


def calculate_summary(df):
    """
    Investment summary.
    """

    if df.empty:

        return {
            "Total Investment": 0.0,
            "Total Return": 0.0,
            "Profit": 0.0,
            "ROI": 0.0,
        }

    investment = float(df["Amount"].sum())

    returns = float(df["Return"].sum())

    profit = returns - investment

    roi = (
        (profit / investment) * 100
        if investment > 0
        else 0.0
    )

    return {
        "Total Investment": investment,
        "Total Return": returns,
        "Profit": profit,
        "ROI": roi,
    }


def category_summary(df):
    """
    Category-wise investment summary.
    """

    if df.empty:

        return pd.DataFrame(
            columns=[
                "Category",
                "Amount",
                "Return",
            ]
        )

    temp = df.copy()

    return (
        temp.groupby(
            "Category",
            as_index=False,
        )[
            [
                "Amount",
                "Return",
            ]
        ]
        .sum()
        .sort_values(
            "Amount",
            ascending=False,
        )
    )


def search_investments(df, keyword):
    """
    Search investments safely.
    """

    if df.empty:
        return df

    if keyword is None:
        return df

    keyword = str(keyword).strip()

    if keyword == "":
        return df

    return df[
        df["Investment"].str.contains(
            keyword,
            case=False,
            regex=False,
            na=False,
        )
  ]
