import numpy as np
import pandas as pd


def formate_col(df, col, type):
    if type == "date":
        df[col] = pd.to_datetime(df[col], errors="coerce").dt.date
    elif type == "num":
        # df[col].astype(str).replace('\.0', '', regex=True)
        df[col] = pd.to_numeric(df[col], errors="coerce", downcast="integer")
    else:
        print("add new type")
    return df


def format(df):
    df.columns = df.columns.str.replace("/ ", "")
    df = df.rename(columns=lambda x: x.replace(" ", "_"))
    df = formate_col(df, "test", "date")
    return df


def clean_num(df):
    filter1 = df["PhoneNumber"] < 1111111111
    filter2 = df["PhoneNumber"].isna()
    df["PhoneNumber"] = np.where(filter1 | filter2, 9999999999, df["PhoneNumber"])
    return df


def last_call(df, tomorrow_str):
    # create table of unique dates
    lc_df = df[df.Last_Call.notna()].copy()
    Last_Call = lc_df["Last_Call"].unique().tolist()
    business_dates = pd.DataFrame(Last_Call, columns=["Last_Call"])
    # calculate true business days from tomorow
    business_dates["age"] = business_dates.Last_Call.apply(
        lambda x: len(pd.bdate_range(x, tomorrow_str))
    )
    business_dates["age"] -= 1
    lc = df.merge(business_dates, on="Last_Call", how="left")

    f1 = lc.Last_Call.isna()
    lc.age = np.where(f1, lc.DaysSinceCreation, lc.age)
    return lc


def checkExtract(df):
    pass


def add_columns(df, tomorrow_str):
    cut_bins = [0, 5, 10, 15, 20, 10000]
    label_bins = [5, 10, 15, 20, 21]
    df["age_category"] = pd.cut(
        df["age"], bins=cut_bins, labels=label_bins, include_lowest=True
    )
    age_sort = {21: 0, 20: 1, 15: 2, 10: 3, 5: 4}
    df["age_sort"] = df["age_category"].map(age_sort)
    ### map
    f1 = df.audit_sort <= 2
    df["sla"] = np.where(f1, 5, 10)
    df["target_sla"] = np.where(f1, 4, 8)
    f1 = df.sla >= df.age
    f2 = df.target_sla >= df.age
    df["meet_sla"] = np.where(f1, 1, 0)
    df["meet_target_sla"] = np.where(f2, 1, 0)
    bucket_amount = 10
    df["togo_bin"] = pd.cut(
        df.ToGoCharts, bins=bucket_amount, labels=[x for x in range(bucket_amount)]
    )
    return df


def clean(df, tomorrow_str):
    f = format(df)
    cn = clean_num(f)
    lc = last_call(cn, tomorrow_str)

    new_col = add_columns(lc, tomorrow_str)
    return new_col
