from dataclasses import dataclass
import pandas as pd
import numpy as np

def rank(df:pd.DataFrame, new_col:str, groups=list(), rank_cols=dict()):
    sort_columns = groups + [*rank_cols.keys()]
    ascending = [True] * len(groups) + [*rank_cols.values()]

    df.sort_values(sort_columns, ascending=ascending, inplace=True)
    df[new_col] = 1
    df[new_col] = df.groupby(groups)[new_col].cumsum()
    return df

def listToString(listValues):
    string = ""
    for i in listValues:
        string += f"'{i}'"
    return f"({string})"

def generateConditionalStatement(group):
    statements = ""
    for i in group['conditions']:
        if i['type'] == "statement":
            statements += f"( {i['column']} {i['condition']} {listToString(i['values'])} )"
        else:
            statements += f" {i['condition']} "
    return statements

@dataclass
class GROUPCONFIG:
    name:str
    priority:int
    conditions:str
    order:dict

def query_df(df:pd.DataFrame, filter_str):
    df.reset_index(drop=True, inplace=True)
    get_index = df.query(filter_str).index
    return df.index.isin(get_index)

def createNewGroupColumn(df:pd.DataFrame, config:GROUPCONFIG):
    get_index = df.query(config.conditions).index
    filters = df.index.isin(get_index)
    df[config.name] = np.where(filters, 1, 0)
    return rank(df, 'score', [config.name], rank_cols=config.order)

def readConfig(config) -> list[GROUPCONFIG]:
    if cfg := config['groupings']:
        return [GROUPCONFIG(
                    name=group['groupName'], 
                    priority=group['priority'],
                    conditions=generateConditionalStatement(group), 
                    order=group['order'])
                    for group in cfg]

def get(df, config):
    if cfgList := readConfig(config['transform']):
        for cfg in cfgList:
            df = createNewGroupColumn(df, cfg)
    return df
