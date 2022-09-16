import json
import os

import numpy as np

from .tables import CONFIG_PATH, tables
from .utils import Business_Days, query_df

bus_day = Business_Days()


def add_filter(filters: list, arg: list):
    # add operator
    if arg[0] == "operator":
        filters.append(arg[1])
    # add operator
    else:
        column, condition, value = arg
        # if value is string add quotes
        if isinstance(value, str):
            value = f"'{value}'"
        # add parentheses
        value = f"({value})"
        # join statement
        f = " ".join([column, condition, value])
        filters.append(f" ({f}) ")
    return filters


def list_to_string(raw_filters):
    filters = []
    # if only one item for filter
    if isinstance(raw_filters[0], str):
        return "".join(add_filter(filters, raw_filters))

    # if nested list, recursive parse
    for filter_ in raw_filters:
        # nested filters
        if isinstance(filter_[0], list):
            filter = " ".join(list_to_string(filter_))
            filters.append(f" ({filter}) ")
        # add filter
        else:
            filters = add_filter(filters, filter_)
    return " ".join(filters)


def create_skill(df, new_skill: str, filters: list):
    clean_filter = list_to_string(filters)
    df.Skill = np.where(query_df(df, clean_filter), new_skill, df.Skill)
    return df


def load_filters():
    default_skills = os.listdir(CONFIG_PATH / "custom_skills")
    with open(CONFIG_PATH / f"default_skills/{max(default_skills)}") as json_file:
        return json.load(json_file)


def complex_skills(df):
    for name, filters in load_filters().items():
        df = create_skill(df, name, filters)
    return df
