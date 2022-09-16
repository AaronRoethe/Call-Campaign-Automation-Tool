import os
from pathlib import Path
from zipfile import ZipFile

import pandas as pd
import pyarrow as pa
import pyarrow.csv as csv

from .utils import Business_Days

paths = Path(__file__).parent.absolute().parent.absolute().parent.absolute()


CONFIG_PATH = paths / "src/config"
TABLE_PATH = paths / "data/table_drop"
LOAD_PATH = paths / "data/load"

Bus_day = Business_Days()


def get_sql_data(local_name, sql, sql_engine) -> pd.DataFrame:
    # update fax query if needed
    try:
        # read if current date
        fax = tables("pull", "na", f"{local_name}_{Bus_day.today_str}.csv")
    except:
        # update & save
        fax = pd.read_sql(sql, sql_engine)
        if rm_files := list(TABLE_PATH.glob(f"{local_name}_*")):
            for file in rm_files:
                os.remove(file)
        tables("push", fax, f"{local_name}_{Bus_day.today_str}.csv")
    return fax


def fallOut(df, file):
    with ZipFile(Path("data/extract") / file, "r") as zip:
        file_name = zip.namelist()[0]
        with zip.open(file_name) as raw_file:
            all_orgs = set([int(line[:8]) for line in raw_file])
    missingIds = list(all_orgs.difference(set(df.Ids)))
    return missingIds


### Input/output static tables ###
def tables(push_pull, table, name, path=Path("data/table_drop")):
    if push_pull == "pull":
        # return csv.read_csv(paths / path / name)
        return pd.read_csv(
            paths / path / name, sep=",", on_bad_lines="warn", engine="python"
        )
    else:
        table.to_csv(TABLE_PATH / name, sep=",", index=False)


def read_compressed(file_path, sep):
    match str(file_path).split(".")[-1]:
        case "zip":
            with ZipFile(file_path, "r") as zip:
                file_name = zip.namelist()[0]
                with zip.open(file_name, "r") as file:
                    return csv.read_csv(
                        file,
                        parse_options=csv.ParseOptions(delimiter=sep, quote_char=False),
                    ).to_pandas()
        case "gz":
            return csv.read_csv(file_path).to_pandas()


def write_compressed(file_path, table):
    match str(file_path).split(".")[-1]:
        case "zip":
            filename = str(file_path).split("\\")[-1][:-4]
            compression_options = dict(method="zip", archive_name=f"{filename}.csv")
            table.to_csv(
                file_path, compression=compression_options, sep=",", index=False
            )
        case "gz":
            try:
                pa_table = pa.Table.from_pandas(table)
            except Exception as e:
                print(e)
            with pa.CompressedOutputStream(file_path, "gzip") as out:
                csv.write_csv(pa_table, out)


# push_pull zip file
def compressed_files(filename, path=Path(LOAD_PATH), table="read", sep=","):
    extract_path = path / filename
    if isinstance(table, str):
        try:
            return read_compressed(extract_path, sep)
        except:
            print("slow")
            return pd.read_csv(extract_path, sep=sep, engine="python", quoting=3)

    elif isinstance(table, pd.DataFrame):
        try:
            write_compressed(extract_path, table)
        except:
            print("slow")
            table.to_csv(extract_path, index=False)
