import numpy as np
import sqlalchemy


def server_insert():
    pass


def clean_for_insert(load):
    int_cols = ["colType"]
    int_key = dict.fromkeys(int_cols, np.int64)
    date_cols = ["colType"]
    date_key = dict.fromkeys(date_cols, "datetime64[ns]")
    return df.astype(dict(int_key, **date_key))


def before_insert(engine: sqlalchemy.engine, remove, lookup) -> None:
    pass


def sql_insert(load, engine: sqlalchemy.engine, table):
    # ask to go forward with insert
    if input("Enter(y/n): ") == "y":
        pass
    else:
        raise SystemExit
    load.to_sql(table, engine, index=False, if_exists="append", schema="dbo")
